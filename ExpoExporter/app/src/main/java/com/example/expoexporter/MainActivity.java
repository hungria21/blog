package com.example.expoexporter;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class MainActivity extends AppCompatActivity {

    private static final int PICK_ZIP_FILE = 1;
    private Button btnSelectZip, btnOpenExpoGo;
    private TextView tvFileName, tvProjectDetails;
    private Uri selectedZipUri;
    private String projectSlug = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btnSelectZip = findViewById(R.id.btnSelectZip);
        btnOpenExpoGo = findViewById(R.id.btnOpenExpoGo);
        tvFileName = findViewById(R.id.tvFileName);
        tvProjectDetails = findViewById(R.id.tvProjectDetails);

        btnSelectZip.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openFilePicker();
            }
        });

        btnOpenExpoGo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openInExpoGo();
            }
        });
    }

    private void openFilePicker() {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("application/zip");
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(Intent.createChooser(intent, "Selecione o código do App (ZIP)"), PICK_ZIP_FILE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PICK_ZIP_FILE && resultCode == Activity.RESULT_OK) {
            if (data != null && data.getData() != null) {
                selectedZipUri = data.getData();
                tvFileName.setText(selectedZipUri.getLastPathSegment());
                analyzeZip(selectedZipUri);
            }
        }
    }

    private void analyzeZip(Uri zipUri) {
        tvProjectDetails.setText("Analisando...");
        btnOpenExpoGo.setVisibility(View.GONE);
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    InputStream inputStream = getContentResolver().openInputStream(zipUri);
                    ZipInputStream zipInputStream = new ZipInputStream(inputStream);
                    ZipEntry entry;
                    String appJsonContent = null;
                    String packageJsonContent = null;

                    while ((entry = zipInputStream.getNextEntry()) != null) {
                        String name = entry.getName();
                        if (name.endsWith("app.json")) {
                            appJsonContent = readStream(zipInputStream);
                        } else if (name.endsWith("package.json")) {
                            packageJsonContent = readStream(zipInputStream);
                        }
                        zipInputStream.closeEntry();
                    }
                    zipInputStream.close();

                    final String result = buildAnalysisResult(appJsonContent, packageJsonContent);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            tvProjectDetails.setText(result);
                            if (!projectSlug.isEmpty()) {
                                btnOpenExpoGo.setVisibility(View.VISIBLE);
                            }
                        }
                    });

                } catch (IOException e) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            tvProjectDetails.setText("Erro ao ler o ZIP: " + e.getMessage());
                        }
                    });
                }
            }
        }).start();
    }

    private String readStream(InputStream inputStream) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line).append("\n");
        }
        return sb.toString();
    }

    private String buildAnalysisResult(String appJson, String packageJson) {
        StringBuilder sb = new StringBuilder();
        sb.append("Resumo da Análise:\n\n");

        if (appJson != null) {
            try {
                JSONObject json = new JSONObject(appJson);
                if (json.has("expo")) {
                    JSONObject expo = json.getJSONObject("expo");
                    sb.append("Nome do Projeto: ").append(expo.optString("name", "N/A")).append("\n");
                    projectSlug = expo.optString("slug", "");
                    sb.append("Slug: ").append(projectSlug).append("\n");
                    sb.append("Versão Expo: ").append(expo.optString("sdkVersion", "N/A")).append("\n");
                }
            } catch (JSONException ignored) {}
        }

        if (packageJson != null) {
            try {
                JSONObject json = new JSONObject(packageJson);
                sb.append("Versão Package: ").append(json.optString("version", "N/A")).append("\n");
            } catch (JSONException ignored) {}
        }

        if (projectSlug.isEmpty()) {
            sb.append("\nStatus: Projeto Expo não identificado no ZIP.\n");
        } else {
            sb.append("\nStatus: Projeto identificado!\n");
            sb.append("Para rodar no Expo Go, o projeto precisa estar sendo servido por um servidor (Ex: Metro Bundler).");
        }

        return sb.toString();
    }

    private void openInExpoGo() {
        if (projectSlug.isEmpty()) return;

        // Tenta abrir o Expo Go usando o esquema exp://
        // Geralmente para projetos locais usamos o IP, mas aqui simulamos a intenção
        String expoUrl = "exp://u.expo.dev/" + projectSlug;
        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(expoUrl));
        try {
            startActivity(intent);
        } catch (Exception e) {
            Toast.makeText(this, "Expo Go não encontrado. Instale-o primeiro.", Toast.LENGTH_LONG).show();
            Intent playStoreIntent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://play.google.com/store/apps/details?id=host.exp.exponent"));
            startActivity(playStoreIntent);
        }
    }
}
