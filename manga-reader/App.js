import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, FlatList, TouchableOpacity, SafeAreaView, StatusBar, Dimensions } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';
import { Plus, Book, Trash2, FileText, ChevronLeft } from 'lucide-react-native';
import Pdf from 'react-native-pdf';
import { WebView } from 'react-native-webview';

export default function App() {
  const [mangas, setMangas] = useState([]);
  const [selectedManga, setSelectedManga] = useState(null);

  useEffect(() => {
    loadMangas();
  }, []);

  const loadMangas = async () => {
    try {
      const mangaDir = FileSystem.documentDirectory + 'mangas/';
      const dirInfo = await FileSystem.getInfoAsync(mangaDir);
      if (!dirInfo.exists) {
        await FileSystem.makeDirectoryAsync(mangaDir, { intermediates: true });
        return;
      }

      const files = await FileSystem.readDirectoryAsync(mangaDir);
      const mangaList = files.map(filename => ({
        id: filename,
        name: filename,
        uri: mangaDir + filename,
        type: filename.toLowerCase().endsWith('.pdf') ? 'pdf' : 'epub'
      }));
      setMangas(mangaList);
    } catch (err) {
      console.error("Error loading mangas:", err);
    }
  };

  const pickDocument = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/pdf', 'application/epub+zip'],
        copyToCacheDirectory: true
      });

      if (!result.canceled) {
        const file = result.assets[0];
        await saveManga(file);
      }
    } catch (err) {
      console.error("Error picking document:", err);
    }
  };

  const saveManga = async (file) => {
    try {
      const mangaDir = FileSystem.documentDirectory + 'mangas/';
      const destination = mangaDir + file.name;
      await FileSystem.copyAsync({
        from: file.uri,
        to: destination
      });
      await loadMangas();
    } catch (err) {
      console.error("Error saving manga:", err);
    }
  };

  const deleteManga = async (manga) => {
    try {
      await FileSystem.deleteAsync(manga.uri);
      await loadMangas();
    } catch (err) {
      console.error("Error deleting manga:", err);
    }
  };

  const renderMangaItem = ({ item }) => (
    <TouchableOpacity onPress={() => setSelectedManga(item)} style={styles.mangaItem}>
      <View style={styles.mangaIcon}>
        {item.type === 'pdf' ? <FileText color="#ff4444" size={32} /> : <Book color="#44aaff" size={32} />}
      </View>
      <View style={styles.mangaInfo}>
        <Text style={styles.mangaName} numberOfLines={1}>{item.name}</Text>
        <Text style={styles.mangaType}>{item.type.toUpperCase()}</Text>
      </View>
      <TouchableOpacity onPress={() => deleteManga(item)} style={styles.deleteButton}>
        <Trash2 color="#999" size={20} />
      </TouchableOpacity>
    </TouchableOpacity>
  );

  if (selectedManga) {
    return (
      <SafeAreaView style={styles.readerContainer}>
        <StatusBar hidden />
        <View style={styles.readerHeader}>
          <TouchableOpacity onPress={() => setSelectedManga(null)} style={styles.backButton}>
            <ChevronLeft color="#fff" size={28} />
          </TouchableOpacity>
          <Text style={styles.readerTitle} numberOfLines={1}>{selectedManga.name}</Text>
        </View>

        {selectedManga.type === 'pdf' ? (
          <Pdf
            source={{ uri: selectedManga.uri }}
            onLoadComplete={(numberOfPages, filePath) => {
              console.log(`Number of pages: ${numberOfPages}`);
            }}
            onPageChanged={(page, numberOfPages) => {
              console.log(`Current page: ${page}`);
            }}
            onError={(error) => {
              console.log(error);
            }}
            onPressLink={(uri) => {
              console.log(`Link pressed: ${uri}`);
            }}
            style={styles.pdf}
            enablePaging={true}
            horizontal={true}
          />
        ) : (
          <WebView
            source={{ uri: selectedManga.uri }}
            style={styles.webview}
          />
        )}
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <View style={styles.header}>
        <Text style={styles.title}>Manga Reader</Text>
        <TouchableOpacity onPress={pickDocument} style={styles.addButton}>
          <Plus color="#fff" size={24} />
        </TouchableOpacity>
      </View>

      {mangas.length === 0 ? (
        <View style={styles.emptyState}>
          <Book color="#333" size={64} />
          <Text style={styles.emptyText}>Nenhum mangá adicionado</Text>
          <TouchableOpacity style={styles.importButton} onPress={pickDocument}>
            <Text style={styles.importButtonText}>Importar PDF ou EPUB</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <FlatList
          data={mangas}
          keyExtractor={(item) => item.id}
          renderItem={renderMangaItem}
          contentContainerStyle={styles.listContainer}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 10,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  addButton: {
    backgroundColor: '#3b82f6',
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContainer: {
    padding: 16,
  },
  mangaItem: {
    flexDirection: 'row',
    backgroundColor: '#1e1e1e',
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
    alignItems: 'center',
  },
  mangaIcon: {
    width: 50,
    height: 50,
    backgroundColor: '#2a2a2a',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  mangaInfo: {
    flex: 1,
    marginLeft: 12,
  },
  mangaName: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  mangaType: {
    color: '#888',
    fontSize: 12,
    marginTop: 2,
  },
  deleteButton: {
    padding: 8,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingBottom: 100,
  },
  emptyText: {
    color: '#666',
    fontSize: 18,
    marginTop: 16,
  },
  importButton: {
    marginTop: 24,
    backgroundColor: '#3b82f6',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  importButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  readerContainer: {
    flex: 1,
    backgroundColor: '#000',
  },
  readerHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: 'rgba(0,0,0,0.8)',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 10,
  },
  backButton: {
    padding: 4,
  },
  readerTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 12,
    flex: 1,
  },
  pdf: {
    flex: 1,
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
    backgroundColor: '#000',
  },
  webview: {
    flex: 1,
    backgroundColor: '#000',
  }
});
