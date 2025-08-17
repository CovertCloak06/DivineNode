package com.divinenode

import android.app.Service
import android.content.Intent
import android.os.IBinder

class VoiceService : Service() {
    override fun onBind(intent: Intent?): IBinder? {
        // Return null if not a bound service
        return null
    }
}
