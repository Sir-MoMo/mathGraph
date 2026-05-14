import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// 1. 初始化 MCP 服务器
const server = new Server(
  {
    name: "mathgraph-tools",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {}, // 声明服务器拥有“工具”调用能力
    },
  }
);

// 2. 定义工具列表：告诉 Gemini 你能做什么
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "calculate_area",
        description: "计算圆形面积的工具",
        inputSchema: {
          type: "object",
          properties: {
            radius: {
              type: "number",
              description: "圆的半径",
            },
          },
          required: ["radius"],
        },
      },
    ],
  };
});

// 3. 实现工具逻辑：当 Gemini 调用工具时执行的操作
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "calculate_area") {
    const radius = request.params.arguments.radius;
    const area = Math.PI * Math.pow(radius, 2);
    
    return {
      content: [
        {
          type: "text",
          text: `半径为 ${radius} 的圆面积是 ${area.toFixed(2)}。`,
        },
      ],
    };
  }
  throw new Error("工具未找到");
});

// 4. 启动服务器（使用标准输入输出与 Continue 通信）
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MATHGRAPH MCP Server 已启动"); // 错误日志会显示在 Continue 的日志窗口
}

main().catch((error) => {
  console.error("启动失败:", error);
  process.exit(1);
});