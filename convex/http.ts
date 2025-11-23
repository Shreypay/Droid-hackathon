import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { api } from "./_generated/api";

const http = httpRouter();

// Create session endpoint
http.route({
  path: "/sessions/create",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.json();
    
    const sessionId = await ctx.runMutation(api.sessions.create, body);
    
    return new Response(JSON.stringify(sessionId), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }),
});

// Get session endpoint
http.route({
  path: "/sessions/{sessionId}",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const sessionId = request.params.sessionId;
    
    const session = await ctx.runQuery(api.sessions.get, {
      sessionId: sessionId as any,
    });
    
    return new Response(JSON.stringify(session), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }),
});

// List sessions endpoint
http.route({
  path: "/sessions/list",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const userId = url.searchParams.get("userId") || "default_user";
    
    const sessions = await ctx.runQuery(api.sessions.list, {
      userId,
    });
    
    return new Response(JSON.stringify(sessions), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }),
});

// CORS preflight
http.route({
  path: "/sessions/create",
  method: "OPTIONS",
  handler: httpAction(async () => {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });
  }),
});

export default http;