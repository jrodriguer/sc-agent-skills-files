# Exploring Pre-Built Skills

## Pre-Built Skills

* [List of Anthropic skills](https://github.com/anthropics/skills/tree/main/skills)  
* [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) 
* [Skill creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)

## Part 1: Updating the Marketing Skill

In the video, we updated the Marketing skill to use the BigQuery MCP server to get data from a BigQuery table instead of requiring a CSV file:

- [Prompts used in this part 1](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/prompts.md#part-1-updating-the-marketing-skill)
- [Updated files of the Marketing skill obtained during filming](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/updated_marketing_skill/analyzing-marketing-campaign/)

You can set up a BigQuery table to try this part (link to instructions below), or you can set up a local database instead. For example, you can set up a local SQLite database, import this [CSV file](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/campaign_performance_4weeks.csv) into the database, and use this [MCP server](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/sqlite). Or you can skip this part entirely.

- Optional: [Instructions for setting up a BigQuery table](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/additional_references/table_setup.md#bigquery-setup)
- Optional alternative: [Instructions for setting up a SQLite table](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/additional_references/table_setup.md#sqlite-setup)

## Part 2: Creating the Brand Guidelines Skill

- [Brand guidelines files](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/brand_guidelines_files/)
- [Prompts used in part 2](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/prompts.md#part-2--creating-the-brand-guideline-skill)
- [Files of the skill obtained during filming](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/brand_guidelines_skill/craftedwell-brand/)

## Part 3: Implementing the Entire Workflow

- [Prompts used in part 3](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/prompts.md#part-3-implementing-the-entire-workflow)
- [Slides obtained during filming](https://github.com/https-deeplearning-ai/sc-agent-skills-files/tree/main/L3/output_report_example/CraftedWell_Weekly_Report_Dec16-22.pptx)

The slides might take a few minutes to generate, and they might look completely different from those in the video.