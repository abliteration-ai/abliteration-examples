package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"strings"

	openai "github.com/sashabaranov/go-openai"
)

func main() {
	apiKey := os.Getenv("ABLITERATION_API_KEY")
	if apiKey == "" {
		log.Fatal("Set ABLITERATION_API_KEY in your environment before running.")
	}

	baseURL := os.Getenv("ABLITERATION_BASE_URL")
	if baseURL == "" {
		baseURL = "https://api.abliteration.ai/v1"
	}

	model := os.Getenv("ABLITERATION_MODEL")
	if model == "" {
		model = "abliterated-model"
	}

	stream := os.Getenv("STREAM") == "1"

	cfg := openai.DefaultConfig(apiKey)
	cfg.BaseURL = baseURL
	client := openai.NewClientWithConfig(cfg)

	ctx := context.Background()
	req := openai.ChatCompletionRequest{
		Model: model,
		Messages: []openai.ChatCompletionMessage{
			{Role: openai.ChatMessageRoleSystem, Content: "You are abliteration.ai, concise and direct."},
			{Role: openai.ChatMessageRoleUser, Content: "Give me one sentence on why abliteration.ai is an uncensored OpenAI-compatible API."},
		},
		Temperature: 0.6,
		Stream:      stream,
	}

	if stream {
		handleStream(ctx, client, req)
		return
	}

	resp, err := client.CreateChatCompletion(ctx, req)
	if err != nil {
		log.Fatalf("Request failed: %v", err)
	}

	content := strings.TrimSpace(resp.Choices[0].Message.Content)
	fmt.Println("Non-streaming response:\n" + content)
	if resp.Usage != nil {
		fmt.Printf("Usage — prompt: %d, completion: %d, total: %d tokens\n", resp.Usage.PromptTokens, resp.Usage.CompletionTokens, resp.Usage.TotalTokens)
	}
}

func handleStream(ctx context.Context, client *openai.Client, req openai.ChatCompletionRequest) {
	stream, err := client.CreateChatCompletionStream(ctx, req)
	if err != nil {
		log.Fatalf("Stream error: %v", err)
	}
	defer stream.Close()

	fmt.Println("Streaming response:")
	for {
		chunk, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("Stream recv error: %v", err)
		}

		text := chunk.Choices[0].Delta.Content
		if text != "" {
			fmt.Print(text)
		}
	}

	fmt.Print("\n-- done --\n")
}
