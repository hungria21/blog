package com.example.alarmapp;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private EditText etInterval;
    private Button btnStart, btnStop;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        etInterval = findViewById(R.id.etInterval);
        btnStart = findViewById(R.id.btnStart);
        btnStop = findViewById(R.id.btnStop);

        btnStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startAlarm();
            }
        });

        btnStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stopAlarm();
            }
        });
    }

    private void startAlarm() {
        String input = etInterval.getText().toString();
        if (input.isEmpty()) {
            Toast.makeText(this, "Insira um intervalo em minutos", Toast.LENGTH_SHORT).show();
            return;
        }

        int minutes = Integer.parseInt(input);
        if (minutes <= 0) {
            Toast.makeText(this, "O intervalo deve ser maior que zero", Toast.LENGTH_SHORT).show();
            return;
        }

        AlarmManager alarmManager = (AlarmManager) getSystemService(Context.ALARM_SERVICE);
        Intent intent = new Intent(this, AlarmReceiver.class);
        intent.putExtra("interval", minutes);

        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            flags |= PendingIntent.FLAG_IMMUTABLE;
        }
        PendingIntent pendingIntent = PendingIntent.getBroadcast(
                this, 0, intent, flags);

        long triggerTime = System.currentTimeMillis() + (minutes * 60 * 1000);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            alarmManager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, triggerTime, pendingIntent);
        } else {
            alarmManager.setExact(AlarmManager.RTC_WAKEUP, triggerTime, pendingIntent);
        }

        SharedPreferences prefs = getSharedPreferences("alarm_prefs", MODE_PRIVATE);
        prefs.edit().putInt("interval", minutes).apply();

        Toast.makeText(this, "Alarme iniciado a cada " + minutes + " minuto(s)", Toast.LENGTH_SHORT).show();
    }

    private void stopAlarm() {
        SharedPreferences prefs = getSharedPreferences("alarm_prefs", MODE_PRIVATE);
        prefs.edit().remove("interval").apply();
        AlarmManager alarmManager = (AlarmManager) getSystemService(Context.ALARM_SERVICE);
        Intent intent = new Intent(this, AlarmReceiver.class);

        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            flags |= PendingIntent.FLAG_IMMUTABLE;
        }
        PendingIntent pendingIntent = PendingIntent.getBroadcast(
                this, 0, intent, flags);

        alarmManager.cancel(pendingIntent);
        Toast.makeText(this, "Alarme parado", Toast.LENGTH_SHORT).show();
    }
}
