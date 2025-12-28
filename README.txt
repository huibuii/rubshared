Conventional Commits 

<type>(<optional scope>): <description>
<optional body>
<optional footer>

______________________________

type:
  - feat
    - add or remove code feature
    - e.g. new code version, new version of scripts etc.
  - fix
    - bug fixes
  - refactor
    - restructure/rewrite code
    - does not change any behaviour of the software
  - style
    - does not affect the meaning
    - e.g. white-space, formatting, missing semi-colons etc.
  - test
    - add missing tests or correcting existing tests
  - docs
    - only affect the documentation
   
scope:
  - any additional information
  - use nouns

description:
  - short message
  - written in the imperative -> "add" instead of "added" or "adds"

body:
  - free form
  - explain the changes and why you made them

footer:
  - references a token
  - story, ticket, ...

______________________________

example:
  - git commit -m "feat: add new function xy" -m "I added this function so we are able to ..."
