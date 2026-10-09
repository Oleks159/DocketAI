# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: llm_extractor.py | Selected source lines: 206-245
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def _new_usage() -> Dict[str, Any]:
    """A fresh, empty usage accumulator. Call this once per file."""
    return {"input_tokens": 0, "output_tokens": 0, "cost": 0.0, "calls": 0}


def _add_usage(total: Dict[str, Any], addition: Optional[Dict[str, Any]]) -> None:
    """Adds one call's usage into a running total (both plain local dicts)."""
    if not addition:
        return
    total["input_tokens"] += addition.get("input_tokens", 0)
    total["output_tokens"] += addition.get("output_tokens", 0)
    total["cost"] += addition.get("cost", 0.0)
    total["calls"] += addition.get("calls", 0)


def _usage_from_gemini(usage_metadata, model: str) -> Dict[str, Any]:
    """Turns one Gemini response's usage_metadata into a plain usage dict."""
    if usage_metadata is None:
        return _new_usage()
    input_tokens = getattr(usage_metadata, "prompt_token_count", 0) or 0
    output_tokens = getattr(usage_metadata, "candidates_token_count", 0) or 0
    cost = config.calculate_cost(input_tokens, output_tokens, model=model)
    logger.debug(f"Call usage -> model={model}, input_tokens={input_tokens}, "
                 f"output_tokens={output_tokens}, cost=${cost:.6f}")
    return {"input_tokens": input_tokens, "output_tokens": output_tokens, "cost": cost, "calls": 1}


def _usage_from_openai(usage_obj, model: str) -> Dict[str, Any]:
    """Turns one OpenAI response's usage object into a plain usage dict."""
    if usage_obj is None:
        return _new_usage()
    input_tokens = getattr(usage_obj, "prompt_tokens", 0) or 0
    output_tokens = getattr(usage_obj, "completion_tokens", 0) or 0
    cost = config.calculate_cost(input_tokens, output_tokens, model=model)
    logger.debug(f"Call usage -> model={model}, input_tokens={input_tokens}, "
                 f"output_tokens={output_tokens}, cost=${cost:.6f}")
    return {"input_tokens": input_tokens, "output_tokens": output_tokens, "cost": cost, "calls": 1}


# ─────────────────────────────────────────────────────────
# END OF EXCERPT. The remaining code is private.
