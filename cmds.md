Below we summarize the concrete syntax of the mainmatter in a Forester tree.
| Function | Meaning |
| --- | --- |
| `\p{...}` | Creates a paragraph containing ...; unlike Markdown, it is mandatory to annotate paragraphs explicitly |
| `\em{...}` | Typesets the content in italics |
| `\strong{...}` | Typesets the content in boldface |
| `\ol{...}` | Creates an ordered list |
| `\ul{...}` | Creates an unordered list |
| `\li{...}` | Creates a list item |
| `#{...}` | Typesets the content in (inline) math mode using KaTeX; note that math mode is idempotent in Forester |
| `##{...}` | Typesets the content in (display) math mode using KaTeX |
| `\transclude{xxx-NNNN}` | Transcludes the tree at address `xxx-NNNN` as a subsection |
| `[title](address)` | Formats the text `title` as a hyperlink to `address`; if `address` is the address of a tree, the link will point to that tree, and otherwise it is treated as a URL |
| `\let\ident[x][y]{body}` | Defines a local function named `\ident` with two arguments; subsequently, the expression `\ident{u}{v}` would expand to `body` with the values of `u,v` substituted for `\x,\y` |
| `\code{...}` | Typesets the content in monospace |
| `\tex{preamble}{body}` | Typesets the body externally using KaTeX using `preamble` as preamble code (e.g. to set up tikz packages, etc.). It can be useful to wrap this in your own macro in order to insert your preamble code automatically. |

- [Build and view your forest for the first time](https://www.forester-notes.org/jms-007D/)
- [Overview of the Forester markup language](https://www.forester-notes.org/jms-007N/)
- [Creating new trees](https://www.forester-notes.org/jms-007H/)
- [Creating your personal biographical tree](https://www.forester-notes.org/jms-007K/)
