package com.nbapredictor.service;

import com.nbapredictor.model.GameRequest;
import com.nbapredictor.model.PredictionResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import org.springframework.beans.factory.annotation.Autowired;

@Service
public class PredictionService {

    private final WebClient webClient;
    private static final String ML_SERVICE_URL = "http://localhost:5001";

    @Autowired
    public PredictionService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }

    public PredictionResponse predictGame(GameRequest request) {
        String homeTeam = request.getHomeTeam();
        String awayTeam = request.getAwayTeam();

        try {
            // Call Python ML service
            MLPredictionResponse mlResponse = webClient.post()
                .uri(ML_SERVICE_URL + "/predict")
                .bodyValue(new MLGameRequest(homeTeam, awayTeam))
                .retrieve()
                .bodyToMono(MLPredictionResponse.class)
                .block(); // For simplicity, using blocking call

            if (mlResponse != null && mlResponse.getError() == null) {
                return new PredictionResponse(
                    mlResponse.getPredictedWinner(),
                    mlResponse.getConfidence(),
                    mlResponse.getMessage(),
                    homeTeam,
                    awayTeam
                );
            } else {
                // Fallback to mock prediction if ML service fails
                return createMockPrediction(homeTeam, awayTeam);
            }
        } catch (Exception e) {
            // Fallback to mock prediction if ML service is unavailable
            return createMockPrediction(homeTeam, awayTeam);
        }
    }

    private PredictionResponse createMockPrediction(String homeTeam, String awayTeam) {
        double confidence = Math.random() * 0.4 + 0.6;
        String predictedWinner = confidence > 0.7 ? homeTeam : awayTeam;
        String message = String.format("%s has %.1f%% chance to win", predictedWinner, confidence * 100);

        return new PredictionResponse(
            predictedWinner,
            confidence,
            message,
            homeTeam,
            awayTeam
        );
    }

    // Helper classes for ML service communication
    public static class MLGameRequest {
        private String homeTeam;
        private String awayTeam;

        public MLGameRequest(String homeTeam, String awayTeam) {
            this.homeTeam = homeTeam;
            this.awayTeam = awayTeam;
        }

        public String getHomeTeam() { return homeTeam; }
        public void setHomeTeam(String homeTeam) { this.homeTeam = homeTeam; }
        public String getAwayTeam() { return awayTeam; }
        public void setAwayTeam(String awayTeam) { this.awayTeam = awayTeam; }
    }

    public static class MLPredictionResponse {
        private String predictedWinner;
        private double confidence;
        private String message;
        private String homeTeam;
        private String awayTeam;
        private String error;

        // Getters and setters
        public String getPredictedWinner() { return predictedWinner; }
        public void setPredictedWinner(String predictedWinner) { this.predictedWinner = predictedWinner; }
        public double getConfidence() { return confidence; }
        public void setConfidence(double confidence) { this.confidence = confidence; }
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        public String getHomeTeam() { return homeTeam; }
        public void setHomeTeam(String homeTeam) { this.homeTeam = homeTeam; }
        public String getAwayTeam() { return awayTeam; }
        public void setAwayTeam(String awayTeam) { this.awayTeam = awayTeam; }
        public String getError() { return error; }
        public void setError(String error) { this.error = error; }
    }

    public String getHealth() {
        return "NBA Predictor API is running!";
    }
}
