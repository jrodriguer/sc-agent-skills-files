# Skills with the Claude API

## Lesson Files

You can find the lesson's notebook and all the required input files <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L5" target="_blank">here</a>.
To run the notebook, you need to create a `.env` file containing an Anthropic API key (no Claude subscription is required):

`ANTHROPIC_API_KEY="your-key"`

You can get a key from <a href="https://platform.claude.com/dashboard" target="_blank">Claude Developer Platform</a>. 

If you choose not to run the notebook, this <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L5/lesson_5.ipynb" target="_blank">notebook</a> displays the cell outputs (as shown in the video). And you can find the generated outputs <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L5/sample_outputs/" target="_blank">here</a>.

## Notes
- Here's the <a href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#pre-installed-libraries" target="_blank">list of pre-installed libraries in the sandboxed environment</a>
- Streaming: The lesson's notebook does not implement streaming with the Messages API. So when you run the cells to get the response, you might need to wait for a few minutes. If you'd like to implement streaming, you can check the documentation <a href="https://platform.claude.com/docs/en/build-with-claude/streaming" target="_blank">here</a>.
- To see more examples of how to use Agent Skills with the API (like multi-turn conversation), make sure to check this <a href="https://platform.claude.com/docs/en/build-with-claude/skills-guide" target="_blank">guide</a>.

## Additional References
- <a href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool" target="_blank">Code Execution Tool</a>
- <a href="https://platform.claude.com/docs/en/build-with-claude/files" target="_blank">Files API</a>
- <a href="https://github.com/anthropics/claude-cookbooks/tree/main/skills" target="_blank">Claude Cookbook: Skills</a>