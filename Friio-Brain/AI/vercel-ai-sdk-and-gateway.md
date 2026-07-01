# Vercel AI SDK and AI Gateway Notes

## Vercel AI SDK

Vercel AI SDK is a TypeScript toolkit for building AI features in web apps and Node.js services.

Main parts:

- `AI SDK Core`: server-side AI calls such as `generateText`, `streamText`, structured output, tool calling, and agent workflows.
- `AI SDK UI`: frontend hooks and helpers for chat interfaces and streaming AI responses.
- `Providers`: model integrations for OpenAI, Anthropic, Google, Azure, Bedrock, Groq, Mistral, DeepSeek, Vercel AI Gateway, and others.

Basic server-side example:

```ts
import { generateText } from "ai";

const { text } = await generateText({
  model: "openai/gpt-4.1",
  prompt: "Explain unit testing in simple words",
});

console.log(text);
```

Useful Friio use cases:

- Customer support assistant for cabin owners.
- Internal admin/backoffice assistant for finding users, cabins, orders, payments, or plowing information.
- Documentation assistant over Friio setup notes, test notes, and API notes.
- Structured extraction from imported reports or support text.
- AI-assisted test generation or explanation for existing xUnit/Vitest tests.

## Vercel AI Gateway

Vercel AI Gateway is a unified API layer for calling many AI models through one endpoint and one key.

Instead of wiring the app directly to OpenAI, Anthropic, Google, or another provider, the app calls AI Gateway and chooses the model by name.

Main benefits:

- One API key for many models.
- Easier model switching with minimal code changes.
- Usage and spend monitoring.
- Budgets and API key controls.
- Fallbacks if one model or provider fails.
- Works with AI SDK, OpenAI-compatible APIs, Python clients, REST, and cURL.

AI SDK example using a Gateway-style model identifier:

```ts
import { generateText } from "ai";

const { text } = await generateText({
  model: "anthropic/claude-opus-4.7",
  prompt: "What is the capital of France?",
});
```

OpenAI-compatible Python example:

```py
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("AI_GATEWAY_API_KEY"),
    base_url="https://ai-gateway.vercel.sh/v1",
)

response = client.chat.completions.create(
    model="openai/gpt-5.5",
    messages=[{"role": "user", "content": "Explain unit tests"}],
)
```

## Practical Friio Direction

For Friio, the clean pattern is:

- Use `AI SDK` in application code for chat, streaming, tool calling, and structured AI output.
- Use `AI Gateway` as the model/provider layer so the app can switch models without rewriting AI features.
- Keep API keys server-side only. Do not expose gateway or provider keys in Remix client code.
- Start with a small server-side route or action before adding a full UI.
- Log prompts, model names, latency, and errors carefully, but do not log secrets or sensitive customer data.
- Add tests around prompt-building, input validation, permission checks, and tool-call behavior.

## Important Notes

- AI features in Friio should respect existing authentication and organization access rules.
- Backoffice AI should not answer with data from another organization unless the current user has access.
- Customer-facing AI should avoid direct write actions at first. Prefer read-only answers or draft suggestions until permissions and audit logs are clear.
- Any AI tool that changes payments, orders, plowing status, contracts, users, or cabin ownership should require explicit user confirmation and backend authorization.
- For imported Broyte.no/Nixus/Friio migration data, AI can help summarize or classify records, but deterministic scripts should remain the source of truth for data-quality checks.

## Official Docs

- Vercel AI SDK: https://ai-sdk.dev/docs/introduction
- Vercel AI Gateway: https://vercel.com/docs/ai-gateway
