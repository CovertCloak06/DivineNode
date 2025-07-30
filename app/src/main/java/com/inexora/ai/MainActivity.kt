package com.inexora.ai

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.TextView
import android.widget.LinearLayout
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL

        val text = TextView(this)
        text.text = "Inexora AI is Ready"
        text.textSize = 20f
        layout.addView(text)

        setContentView(layout)

        Toast.makeText(this, "Welcome to Inexora AI", Toast.LENGTH_LONG).show()
    }
}
