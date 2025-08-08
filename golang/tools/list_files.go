package tools

import (
	"encoding/json"
	"os"
	"path/filepath"

	"github.com/anthropics/anthropic-sdk-go"
)

// ListFilesTool implements the list_files functionality
type ListFilesTool struct {
	inputSchema anthropic.ToolInputSchemaParam
}

// ListFilesInput represents the input parameters for the list_files tool
type ListFilesInput struct {
	Path string `json:"path,omitempty" jsonschema_description:"Optional relative path to list files from. Defaults to current directory if not provided."`
}

// NewListFilesTool creates a new instance of the list files tool
func NewListFilesTool() *ListFilesTool {
	return &ListFilesTool{
		inputSchema: GenerateSchema[ListFilesInput](),
	}
}

// Name returns the tool name
func (t *ListFilesTool) Name() string {
	return "list_files"
}

// Description returns the tool description
func (t *ListFilesTool) Description() string {
	return "List files and directories at a given path. If no path is provided, lists files in the current directory."
}

// InputSchema returns the JSON schema for tool input validation
func (t *ListFilesTool) InputSchema() anthropic.ToolInputSchemaParam {
	return t.inputSchema
}

// Execute lists all files and directories in the specified path
func (t *ListFilesTool) Execute(input json.RawMessage) (string, error) {
	var listFilesInput ListFilesInput
	err := json.Unmarshal(input, &listFilesInput)
	if err != nil {
		return "", err
	}

	dir := "."
	if listFilesInput.Path != "" {
		dir = listFilesInput.Path
	}

	var files []string
	err = filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		relPath, err := filepath.Rel(dir, path)
		if err != nil {
			return err
		}

		if relPath != "." {
			if info.IsDir() {
				files = append(files, relPath+"/")
			} else {
				files = append(files, relPath)
			}
		}
		return nil
	})

	if err != nil {
		return "", err
	}

	result, err := json.Marshal(files)
	if err != nil {
		return "", err
	}

	return string(result), nil
}
