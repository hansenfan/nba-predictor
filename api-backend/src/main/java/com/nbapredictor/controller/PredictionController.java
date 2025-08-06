package com.nbapredictor.controller;

import com.nbapredictor.model.GameRequest;
import com.nbapredictor.model.PredictionResponse;
import com.nbapredictor.service.PredictionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/predictions")
@CrossOrigin(origins = "*")
public class PredictionController {

    @Autowired
    private PredictionService predictionService;

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok(predictionService.getHealth());
    }

    @GetMapping("/hello")
    public ResponseEntity<String> sayHello() {
        return ResponseEntity.ok("Hello from NBA Predictor API!");
    }

    @PostMapping("/predict")
    public ResponseEntity<PredictionResponse> predictGame(@RequestBody GameRequest request) {
        try {
            PredictionResponse prediction = predictionService.predictGame(request);
            return ResponseEntity.ok(prediction);
        } catch (Exception e) {
            PredictionResponse errorResponse = new PredictionResponse(
                "Error",
                0.0,
                "Failed to make prediction: " + e.getMessage(),
                request.getHomeTeam(),
                request.getAwayTeam()
            );
            return ResponseEntity.badRequest().body(errorResponse);
        }
    }
}
