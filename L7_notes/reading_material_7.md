# Skills with the Claude Agent SDK

## Lesson's Files

You can find all the files for L7 <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7" target="_blank">here</a>. Here are some highlighted files:
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/prompts" target="_blank">System prompts for the main agent and subagents</a>
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/.claude/skills/learning-a-tool/" target="_blank">Files for the `learning-a-tool` skill</a>
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/utils.py" target="_blank">utils.py</a> (message formatting)
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/agent.py" target="_blank">agent.py</a>
- <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7_notes/learning-mineru/" target="_blank">The learning guide generated during filming</a>

To run the agent, follow the instructions in the <a href="https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L7/README.md" target="_blank">README file</a>.

### Prompts Used in the Lesson

- `Help me get started with MinerU. Create a learning guide. Show me your plan first.`

    - **Note**: The agent might take around 15 minutes to finish. You can always update the skill's instructions and agent definitions if you want the research to be faster or the learning guide to be simpler. You can also try running the subagents with Haiku.

- For the MCP part (which you can skip if you wish):

    `Write ./learning-mineru/resources.md to the "Resources" subpage under Learning in Notion. The subpage already exists. Use rich formatting. For Notion MCP: You can use the full range of Notion block types for proper formatting.`
   
   In the Notion account we used in the lesson, we created a page called `Learning` and added a subpage called `Resources`.

## More Advanced Options

- <a href="https://platform.claude.com/docs/en/agent-sdk/python#example-advanced-permission-control" target="_blank">Advanced Permission Control</a>
- <a href="https://platform.claude.com/docs/en/agent-sdk/python#building-a-continuous-conversation-interface" target="_blank">Building a Continuous Conversation Interface (interrupt, new conversation, exit)</a>


## References

- <a href="https://platform.claude.com/docs/en/agent-sdk/overview" target="_blank">Claude Agent SDK Documentation</a>
- <a href="https://platform.claude.com/docs/en/agent-sdk/python" target="_blank">Python Agent SDK</a>
- <a href="https://platform.claude.com/docs/en/agent-sdk/skills" target="_blank">Agent Skills in the SDK</a>
- <a href="https://github.com/anthropics/claude-agent-sdk-demos" target="_blank">Claude Agent SDK Demos</a>