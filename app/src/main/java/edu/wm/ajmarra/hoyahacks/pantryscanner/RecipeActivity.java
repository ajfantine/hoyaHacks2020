package edu.wm.ajmarra.hoyahacks.pantryscanner;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class RecipeActivity extends AppCompatActivity {

    Button button1, button2;

    WebView recipeView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.recipe_activity);

        recipeView = findViewById(R.id.recipeview);
        WebSettings webSettings = recipeView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        recipeView.loadUrl("http://10.150.237.154:5000/get-reccomendation/");
        recipeView.setWebViewClient(new WebViewClient());

        button1 = findViewById(R.id.button1);
        button1.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent i = new Intent(RecipeActivity.this, PantryActivity.class);
                startActivity(i);
            }
        });

        button2 = findViewById(R.id.button2);
        button2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent i = new Intent(RecipeActivity.this, ScanActivity.class);
                startActivity(i);
            }
        });

    }
}
