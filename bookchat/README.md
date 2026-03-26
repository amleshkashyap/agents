### Outputs

  * Using OpenAI model and embedding

```

================================ Human Message =================================

As per the document, list some 10 annotations?
================================== Ai Message ==================================
Tool Calls:
  retrieve_context (call_GJvAWwWBVANv34Qsvj2ev6AR)
 Call ID: call_GJvAWwWBVANv34Qsvj2ev6AR
  Args:
    query: list 10 annotations
================================== Ai Message ==================================

Here are 10 annotations mentioned in the document:

1. @Transactional: Manages transactions at the method or class level.
2. @Query("SELECT u FROM User u WHERE u.email = ?1"): Custom JPA queries.
3. @Modifying: Used for update/delete queries.
4. @EnableJpaRepositories: Enables Spring Data JPA repositories.
5. @Param: Binds method parameters to query parameters in @Query.
6. @NotBlank: Ensures that a string is not null or empty (trims leading and trailing spaces).
7. @NotEmpty: Ensures a collection, map, or array is not empty.
8. @Min(value): Validates that a numeric field is greater than or equal to the specified value.
9. @Max(value): Validates that a numeric field is less than or equal to the specified value.
10. @Email: Ensures that a string is a valid email address.

```


  * Using Ollama with llama3.2
    - Ollama sends a dictionary in the parameter `query` in the tool, instead of string
    - Upto 5x slower than OpenAI

```
================================ Human Message =================================

As per the document, list some 10 annotations?
================================== Ai Message ==================================

{"name": "retrieve_context", "parameters": {"object": "<nil>", "query": {"annotations": ["BOLD", "ITALICS", "UNDERLINE", "STRIKETHROUGH", " superscript", "subscript", "small text", "big text", "code", "link"]}}
```

### LangFuse
  * Outputs
    - All the steps involved, eg, model call, tool call, context retrieval
      - eg, start -> model -> tool -> model -> end
    - Time spent in each of the above steps
    - Money spent in each of the above steps
    - Response metadata, eg, completion tokens, prompt tokens, reasoning tokens, temperature
    - Functional outputs from langfuse
      - LLM as a judge - provides some kind of score and a comment
