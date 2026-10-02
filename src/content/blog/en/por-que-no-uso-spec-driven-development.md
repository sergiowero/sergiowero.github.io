---
title: "Why I Don't Use Spec-Driven Development, and Neither Should You"
description: "SDD promises to bring order to AI-assisted programming. In practice, I prefer iterating on code and tests."
pubDate: 2026-09-27
tags: ["AI", "spec-driven-development", "software engineering", "opinion"]
draft: false
---

## TL;DR

Spec-Driven Development, or SDD, is probably the most popular approach you see on social media. When I browsed Facebook, I came across ads for courses telling you not to fall behind and to learn SDD. They try to scare you into buying the idea by playing on FOMO. That's another story, though. What stands out to me is how social media has been flooded with a methodology that, in my opinion, hasn't been sufficiently tested and is simply presented as the "popular" choice.

Personally, I prefer to write prompts that are as well-defined as possible, with clear goals, and then use plan mode or refine the initial prompt in a chat. That has worked better for me and lets me move faster. As long as the code works and is well structured, today's models, both frontier and non-frontier, can read and understand it. Creating a spec and keeping it in the codebase is a lot like extensively commenting all your code before the AI era: eventually, the code changes and the comments get forgotten. Keeping them up to date means extra work to keep two separate things in sync. Maybe that's why no company I've worked for has required every line of code to be documented. In the end, that slows the process down, and I think SDD does the same.

That said, to offer a bit of balance, I do think it can be worth taking the time to write a spec upfront in highly complex projects with a lot of interdependence between services, and to try to cover as many edge cases as possible from the start.

## My experience

None of the companies I've worked for this year used SDD. At each one, people did the best they could with Claude Code, without clear training or best practices. At least I'm lucky that my employer provides training to help me learn how to use these harnesses.

On the other hand, I tried it in personal projects: a video game and my open-source project, Agent Q. I gave up quickly on the game because I'm making it with vibe coding and, honestly, I don't have clear specs. But Agent Q seemed like a good fit for SDD: it's a smaller, less ambitious project, and the hype online was through the roof. I started with OpenSpec; it was the first tool I found, and my company had also hosted a talk about it. At first, I thought it was great: it felt like all my specs were being implemented on the first try, with very little rework.

Then I noticed something that left me stunned: I started accumulating what seemed like an absurd number of spec files. There were around 200 files after just two days of work.

The coworkers who gave a talk about it at work said it was a way to prevent hallucinations, but I think they were wrong. Hallucinations kept happening as usual: the model added or left things out, whether I used SDD or not.

That's why I wanted to write this: to lay out the downsides of this methodology and, above all, to complain a little about the hype and FOMO that internet snake-oil salespeople use to sell their SDD courses.

## So what is SDD?

I'm not the best person to explain SDD or give the definitive definition, so I'll leave it to everyone to look it up; that's not the point of this post. But here's a quick summary.

With SDD, before writing code, you first define the spec. Then the spec is used as the basis for implementing the code, with the idea that AI agents can code more accurately and avoid sloppy implementations that need refactoring later.

The idea is: plan -> tasks -> code.

OpenSpec helps you write specs, which can be good or bad. Sometimes it does a great job, and sometimes it makes things up. The best approach is to give it as much context and as many requirements as you can, then let OpenSpec improve them and turn them into a plan.

## Debunking SDD's promises

You can distill several promises from SDD: these are the arguments people usually make for why it's good. To me, it's a double-edged sword, and here's why.

| Promise | My take |
|---|---|
| It helps produce better requirements and find edge cases before implementation | There's some truth to this, but if you let AI generate the requirements, you'll end up with incomplete requirements you didn't need in the first place |
| Specs are written down in files in the project, giving agents better context | Specs aren't the source of truth; in the end, code always wins that contest. Relying on outdated specs can cause more problems in the long run |
| Specs make decisions traceable | Do you really need traceability for changes? That's what Git is for |
| They leave an audit trail that can be reviewed | Git, again |
| Other agents or people can pick up the task without being tied to a particular model | Again, relying on AI-generated specs can produce code you don't need. You can also do this with a Jira ticket or a well-written issue. You don't need a spec in the codebase to pick up a task |

## Why I stopped using it in personal projects

In my personal projects, I deleted almost all the specs that had piled up and went back to working directly with Claude, Codex, and OpenCode. I use plan mode and goal mode whenever needed, along with project-specific custom skills, and I get things done much faster.

If I had to list the reasons, they'd be something like this:

- It slows me down; plan mode and direct mode work better.
- It generates lots of Markdown files that don't get used in later sessions. The model prefers to go straight to the code, and so do I.
- Hallucinations keep happening just as often.
- Git is my change-tracking tool; I don't need specs.

### Spec drift

While searching online, I came across the term "spec drift." It's what happens when a spec falls out of sync because the code changes without the spec being updated.

This happens even when you try to follow the SDD workflow correctly. Small fixes or changes from other sessions can still go unnoticed in the current session and therefore never make it into the spec. Even OpenSpec tells you not to create a spec for a trivial change. Seriously? They're encouraging spec drift themselves. If the spec can't be the source of truth, why have it in your project?

In my view, code will always be the real source of truth. Today's models can read code and understand its intent very well. What happens if an agent reads the spec, sees one thing, and then finds a contradiction in the code? A model can't really tell which one is right; it'll simply pick one "truth" at random. The same thing happens if you put contradictory instructions in an AGENTS.md file: the model chooses which ones to follow.

> *Spec drift*: the code changes, the Markdown doesn't.

### The spec doesn't produce deterministic code

A model will never generate the same code every time from a spec. I think people are trying to make this happen, but it's not possible right now.

### Reviewing Markdown isn't reviewing software

What if I need to investigate a bug?

Let's say I want to fix a bug. What should I do? First, figure out what's going wrong. There are many kinds of bugs, but two examples come to mind: an unhandled exception and incorrect behavior.

#### Incorrect behavior

For incorrect behavior, the bug report itself already tells you what's going wrong. For example: "the total is calculated incorrectly," "the new item doesn't appear in the list," or "the item appears twice." In these cases, I find it highly unlikely that the bug will be fixed by adding a clause to the spec, such as "items must appear only once." And in the case of the missing item, the spec probably already says that new items should appear in the list. The spec doesn't help much with finding the bug. It's better to go straight to the code, find the relevant part, and fix it. Reviewing the spec is unnecessary; you'll have to look at the code to find the cause anyway.

#### Exceptions / crashes

Here, a spec is of no use at all when it comes to tracking down an exception or a crash. The right thing to do is go straight to the code, find the error, and apply a fix, whether that's a small change or a complete refactor. A spec doesn't help maintain products in production.

## My own way of working

In the end, every project is different, but in general, what works for me is simple: I give my agent a clear goal and instructions on how to approach it. I tell it how to verify that the task is done, and if the task calls for it, I start with plan mode to make sure it's actually going to do what I want.

This is all pretty standard advice when you start coding with these tools. But little by little, you figure out how to refine your prompts and get more out of them.

To sum it up, my prompts include:

- A clear, well-defined goal.
- Acceptance / validation criteria: what needs to happen for the task to be considered done.
- Steering: any additional instructions that help guide the model in the right direction.
- Guardrails: constraints, things it must not touch, and commands I don't want it to run.

With this simple approach, I can work quickly. The models understand the task and implement it. If there's a simple error, I fix it in the same session. If there's a bigger problem, I start a new session and provide a complete prompt like the one above.

It's also helped me to open sessions just to refine my prompt. If you do this inside the same project with Claude Code or Codex, the models explore the project to create a better prompt. In a later post, I'll explain this preferred format for refining prompts in more detail. There's nothing extraordinary about it; it just saves me a few keystrokes.

## Conclusion

My conclusion is blunt and simple: SDD encourages you to make agent-assisted programming feel like writing a document, but without any real benefit.

I think SDD became so popular because of the AI hype, but in reality, it's not a mature methodology and doesn't have years of evidence behind it to show that following it helps.

It's better to keep prompts clear and well structured, and to remember that AI is still nondeterministic. Adding a layer of Markdown doesn't make it deterministic, no matter how much SDD's most ardent supporters might wish otherwise.

I invite everyone who read this to think about SDD and question what they believe works and what doesn't.
