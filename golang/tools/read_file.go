package tools

import (
	"encoding/json"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

// ReadFileTool implements the read_file functionality
type ReadFileTool struct {
	inputSchema anthropic.ToolInputSchemaParam
}

// ReadFileInput represents the input parameters for the read_file tool
type ReadFileInput struct {
	Path string `json:"path" jsonschema_description:"The relative path of a file in the working directory."`
}

// NewReadFileTool creates a new instance of the read file tool
func NewReadFileTool() *ReadFileTool {
	return &ReadFileTool{
		inputSchema: GenerateSchema[ReadFileInput](),
	}
}

// Name returns the tool name
func (t *ReadFileTool) Name() string {
	return "read_file"
}

// Description returns the tool description
func (t *ReadFileTool) Description() string {
	return "Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names."
}

// InputSchema returns the JSON schema for tool input validation
func (t *ReadFileTool) InputSchema() anthropic.ToolInputSchemaParam {
	return t.inputSchema
}

// Execute reads the contents of a file at the specified path
func (t *ReadFileTool) Execute(input json.RawMessage) (string, error) {
	var readFileInput ReadFileInput
	err := json.Unmarshal(input, &readFileInput)
	if err != nil {
		return "", err
	}

	content, err := os.ReadFile(readFileInput.Path)
	if err != nil {
		return "", err
	}
	return string(content), nil
}
