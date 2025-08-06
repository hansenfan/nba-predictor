package com.nbapredictor.model;

public class PredictionResponse {
    private String predictedWinner;
    private double confidence;
    private String message;
    private String homeTeam;
    private String awayTeam;

    public PredictionResponse() {}

    public PredictionResponse(String predictedWinner, double confidence, String message, String homeTeam, String awayTeam) {
        this.predictedWinner = predictedWinner;
        this.confidence = confidence;
        this.message = message;
        this.homeTeam = homeTeam;
        this.awayTeam = awayTeam;
    }

    public String getPredictedWinner() {
        return predictedWinner;
    }

    public void setPredictedWinner(String predictedWinner) {
        this.predictedWinner = predictedWinner;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getHomeTeam() {
        return homeTeam;
    }

    public void setHomeTeam(String homeTeam) {
        this.homeTeam = homeTeam;
    }

    public String getAwayTeam() {
        return awayTeam;
    }

    public void setAwayTeam(String awayTeam) {
        this.awayTeam = awayTeam;
    }
}
