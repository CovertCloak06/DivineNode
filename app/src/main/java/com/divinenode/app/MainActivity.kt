package com.divinenode.app

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
        text.text = getString(R.string.parakeleon_welcome)
        text.textSize = 20f
        layout.addView(text)

        setContentView(layout)

        Toast.makeText(this, "Welcome to DivineNode • Parakeleon", Toast.LENGTH_LONG).show()
    }
}