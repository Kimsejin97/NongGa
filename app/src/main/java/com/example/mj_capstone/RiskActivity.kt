package com.example.mj_capstone

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class RiskActivity : AppCompatActivity(){



    override fun onCreate(savedInstanceState: Bundle?){
        super.onCreate(savedInstanceState)
        setContentView((R.layout.activity_risk))

        val actionbar = supportActionBar
        actionbar!!.title = "농산물 위험도"
        actionbar.setDisplayHomeAsUpEnabled(true)
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }
}