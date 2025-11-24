import "dotenv/config";
import OpenAI from "openai";

const apiKey = process.env.ABLITERATION_API_KEY;
if (!apiKey) {
  console.error("Set ABLITERATION_API_KEY in .env or your shell before running.");
  process.exit(1);
}

const client = new OpenAI({
  apiKey,
  baseURL: process.env.ABLITERATION_BASE_URL || "https://api.abliteration.ai/v1",
});

const model = process.env.ABLITERATION_MODEL || "abliterated-model";
const stream = process.env.STREAM === "1";

async function main() {
  const payload = {
    model,
    messages: [
      { role: "system", content: "You are abliteration.ai, concise and direct." },
      { role: "user", content: "Give me one sentence on why abliteration.ai is an uncensored OpenAI-compatible API." },
    ],
    temperature: 0.6,
  };

  if (stream) {
    const streamResp = await client.chat.completions.create({ ...payload, stream: true });
    process.stdout.write("Streaming response:\n");
    for await (const chunk of streamResp) {
      const text = chunk.choices?.[0]?.delta?.content || "";
      if (text) process.stdout.write(text);
    }
    process.stdout.write("\n\n-- done --\n");
    return;
  }

  const completion = await client.chat.completions.create(payload);
  const message = completion.choices?.[0]?.message?.content || "(no content returned)";
  console.log("Non-streaming response:\n" + message);
  if (completion.estimated_credits_used !== undefined) {
    console.log(`Estimated credits used: ${completion.estimated_credits_used}`);
  }
  if (completion.estimated_cost_usd !== undefined) {
    console.log(`Estimated cost (USD): ${completion.estimated_cost_usd}`);
  }
  if (completion.remaining_credits !== undefined) {
    console.log(`Remaining credits: ${completion.remaining_credits}`);
  }
}

main().catch((err) => {
  console.error("Request failed", err);
  process.exit(1);
});
