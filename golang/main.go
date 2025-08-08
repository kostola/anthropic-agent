package main

import (
	"bufio"
	"context"
	"fmt"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/kostola/anthropic-agent/agent"
	"github.com/kostola/anthropic-agent/tools"
)

func main() {
	client := anthropic.NewClient()

	scanner := bufio.NewScanner(os.Stdin)
	getUserMessage := func() (string, bool) {
		if !scanner.Scan() {
			return "", false
		}
		return scanner.Text(), true
	}

	agentTools := []agent.ToolDefinition{
		tools.NewReadFileTool(),
		tools.NewListFilesTool(),
	}

	agentInstance := agent.New(&client, getUserMessage, agentTools)
	err := agentInstance.Run(context.TODO())
	if err != nil {
		fmt.Printf("Error: %s\n", err.Error())
	}
}
