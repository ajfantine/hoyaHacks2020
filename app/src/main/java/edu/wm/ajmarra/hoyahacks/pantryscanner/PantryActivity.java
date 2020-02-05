package edu.wm.ajmarra.hoyahacks.pantryscanner;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class PantryActivity extends AppCompatActivity {
    Button button1, button2;
    WebView pantryView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.pantry_activity);

        pantryView = findViewById(R.id.pantryview);
        WebSettings webSettings = pantryView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        pantryView.loadUrl("http://10.150.237.154:5000/display-database/");
        pantryView.setWebViewClient(new WebViewClient());

        button1 = findViewById(R.id.button1);
        button1.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent i = new Intent(PantryActivity.this, ScanActivity.class);
                startActivity(i);
            }
        });

        button2 = findViewById(R.id.button2);
        button2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent i = new Intent(PantryActivity.this, RecipeActivity.class);
                startActivity(i);
            }
        });

    }
}
