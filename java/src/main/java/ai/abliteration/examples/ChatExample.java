package ai.abliteration.examples;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public class ChatExample {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("ABLITERATION_API_KEY");
        if (apiKey == null || apiKey.isBlank()) {
            System.err.println("Set ABLITERATION_API_KEY in your environment before running.");
            System.exit(1);
        }

        String baseUrl = System.getenv().getOrDefault("ABLITERATION_BASE_URL", "https://api.abliteration.ai/v1");
        String model = System.getenv().getOrDefault("ABLITERATION_MODEL", "abliterated-model");
        boolean stream = "1".equals(System.getenv("STREAM"));

        String payload = buildPayload(model, stream);

        HttpClient client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/chat/completions"))
                .timeout(Duration.ofSeconds(60))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + apiKey)
                .POST(HttpRequest.BodyPublishers.ofString(payload))
                .build();

        if (stream) {
            streamResponse(client, request);
        } else {
            runOnce(client, request);
        }
    }

    private static String buildPayload(String model, boolean stream) {
        StringBuilder sb = new StringBuilder();
        sb.append("{\"model\":\"").append(model).append("\",");
        sb.append("\"messages\":[");
        sb.append("{\"role\":\"system\",\"content\":\"You are abliteration.ai, concise and direct.\"},");
        sb.append("{\"role\":\"user\",\"content\":\"Give me one sentence on why abliteration.ai is an uncensored OpenAI-compatible API.\"}");
        sb.append("],\"temperature\":0.6");
        if (stream) {
            sb.append(",\"stream\":true");
        }
        sb.append("}");
        return sb.toString();
    }

    private static void runOnce(HttpClient client, HttpRequest request) throws IOException, InterruptedException {
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() >= 300) {
            System.err.printf("Request failed (status %d): %s%n", response.statusCode(), response.body());
            System.exit(1);
        }

        String body = response.body();
        try {
            JsonNode node = MAPPER.readTree(body);
            String content = node.path("choices").get(0).path("message").path("content").asText("(no content returned)");
            System.out.println("Non-streaming response:\n" + content);

            JsonNode usage = node.path("usage");
            if (usage.isObject()) {
                int prompt = usage.path("prompt_tokens").asInt(-1);
                int completion = usage.path("completion_tokens").asInt(-1);
                int total = usage.path("total_tokens").asInt(-1);
                System.out.printf("Usage — prompt: %d, completion: %d, total: %d tokens%n", prompt, completion, total);
            }
        } catch (Exception ex) {
            System.err.println("Failed to parse response: " + ex.getMessage());
            System.err.println(body);
            System.exit(1);
        }
    }

    private static void streamResponse(HttpClient client, HttpRequest request) throws IOException, InterruptedException {
        HttpResponse<InputStream> response = client.send(request, HttpResponse.BodyHandlers.ofInputStream());
        if (response.statusCode() >= 300) {
            String body = new String(response.body().readAllBytes(), StandardCharsets.UTF_8);
            System.err.printf("Request failed (status %d): %s%n", response.statusCode(), body);
            System.exit(1);
        }

        System.out.println("Streaming response:");
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(response.body()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.startsWith("data:")) {
                    continue;
                }
                String data = line.substring(5).trim();
                if (data.isBlank()) {
                    continue;
                }
                if ("[DONE]".equals(data)) {
                    break;
                }
                try {
                    JsonNode node = MAPPER.readTree(data);
                    String delta = node.path("choices").get(0).path("delta").path("content").asText("");
                    System.out.print(delta);
                } catch (Exception ex) {
                    System.err.println("\nFailed to parse chunk: " + ex.getMessage());
                    System.err.println(data);
                }
            }
        }

        System.out.println("\n-- done --");
    }
}
