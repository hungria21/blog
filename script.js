document.addEventListener('DOMContentLoaded', () => {
    const keys = document.querySelectorAll('.key');
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();

    const notes = {
        'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63,
        'F4': 349.23, 'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00,
        'A#4': 466.16, 'B4': 493.88, 'C5': 523.25
    };

    const songs = {
        'cornfield-chase': [
            { note: 'A4', duration: 500 }, { note: 'G4', duration: 500 }, { note: 'A4', duration: 500 }, { note: 'C5', duration: 500 },
            { note: 'A4', duration: 500 }, { note: 'G4', duration: 500 }, { note: 'A4', duration: 500 }, { note: 'B4', duration: 500 },
        ],
        'no-time-for-caution': [
            { note: 'C4', duration: 150 }, { note: 'D4', duration: 150 }, { note: 'E4', duration: 150 }, { note: 'C4', duration: 150 },
            { note: 'D4', duration: 150 }, { note: 'E4', duration: 150 }, { note: 'C4', duration: 150 }, { note: 'D4', duration: 150 },
            { note: 'E4', duration: 150 }, { note: 'C4', duration: 150 }, { note: 'D4', duration: 150 }, { note: 'E4', duration: 150 },
        ],
        'main-theme': [
            { note: 'A4', duration: 400 }, { note: 'E4', duration: 400 }, { note: 'A4', duration: 400 }, { note: 'G4', duration: 400 },
            { note: 'A4', duration: 400 }, { note: 'D4', duration: 400 }, { note: 'A4', duration: 400 }, { note: 'C4', duration: 400 },
        ]
    };

    keys.forEach(key => {
        key.addEventListener('click', () => playNote(key));
    });

    document.querySelectorAll('.songs button').forEach(button => {
        button.addEventListener('click', () => playSong(songs[button.id]));
    });

    function playNote(key) {
        const note = key.dataset.note;
        const frequency = notes[note];
        if (!frequency) return;

        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.type = 'sine';
        oscillator.frequency.value = frequency;
        gainNode.gain.setValueAtTime(0.5, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 1);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 1);

        key.classList.add('active');
        setTimeout(() => key.classList.remove('active'), 200);
    }

    function playSong(song) {
        if (audioContext.state === 'suspended') {
            audioContext.resume();
        }

        let delay = 0;
        song.forEach(noteInfo => {
            setTimeout(() => {
                const key = document.querySelector(`[data-note="${noteInfo.note}"]`);
                if (key) {
                    playNote(key);
                }
            }, delay);
            delay += noteInfo.duration;
        });
    }
});
