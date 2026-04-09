"""Prompt templates for CUAD clause extraction and CaseHOLD precedent ranking.

Follows Anthropic prompt engineering best practices:
  - External knowledge restriction (reduce hallucinations)
  - Verify with citations (mandatory word-for-word quotes)
  - Iterative refinement for high-stakes clauses
  - Structured JSON output

System prompt base: julia/src/completion.ts:buildLegalSystemPrompt()

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

# ── CUAD System Prompt ─────────────────────────────────────────

CUAD_SYSTEM_PROMPT = """\
You are Julia, a legal analysis assistant. Analyze ONLY the contract text provided below.

CRITICAL CONSTRAINTS:
- Do NOT use your general knowledge about contracts.
- Do NOT infer clauses that are not explicitly stated in the contract text.
- If a clause type is not present in the contract, respond with found: false.
- Do NOT fabricate a plausible clause — only extract text that literally appears in the contract.
- All extracted text MUST be word-for-word quotes from the contract.
- Never provide legal advice — frame all outputs as analysis only.

For each clause you extract:
1. Provide the EXACT text from the contract (word-for-word quote).
2. Provide the section/paragraph reference where it appears.
3. If you cannot find a word-for-word quote, you MUST set found to false.\
"""

# ── CUAD Single Clause Extraction ──────────────────────────────

CUAD_EXTRACT_SINGLE = """\
Given the following contract text, extract the clause of type "{clause_type}".

Respond with ONLY a JSON object (no markdown, no explanation) in this exact format:
{{
  "clause_type": "{clause_type}",
  "found": true or false,
  "extracted_text": "exact word-for-word quote from contract" or null,
  "section_reference": "section number or paragraph reference" or null,
  "confidence": 0.0 to 1.0,
  "verification": "verified" or "retracted" or "not_applicable"
}}

If the clause type is NOT present in the contract, respond with:
{{
  "clause_type": "{clause_type}",
  "found": false,
  "extracted_text": null,
  "section_reference": null,
  "confidence": 1.0,
  "verification": "not_applicable"
}}

CONTRACT TEXT:
{contract_text}\
"""

# ── CUAD Iterative Verification (high-stakes clauses) ─────────

CUAD_VERIFY_EXTRACTION = """\
You previously extracted the following clause from a contract.
Verify that the extracted text appears EXACTLY (word-for-word) in the original contract.

CLAUSE TYPE: {clause_type}
EXTRACTED TEXT: {extracted_text}
SECTION REFERENCE: {section_reference}

ORIGINAL CONTRACT TEXT:
{contract_text}

Respond with ONLY a JSON object:
{{
  "clause_type": "{clause_type}",
  "found": true or false,
  "extracted_text": "corrected exact quote" or null,
  "section_reference": "corrected reference" or null,
  "confidence": 0.0 to 1.0,
  "verification": "verified" if quote matches, "retracted" if it does not
}}

If the extracted text does NOT appear word-for-word in the contract, you MUST set
verification to "retracted" and found to false.\
"""

# ── CUAD Batch Extraction ─────────────────────────────────────

CUAD_EXTRACT_BATCH = """\
Given the following contract text, extract ALL of the following clause types.
For each clause type, determine if it is present and extract the exact text.

CLAUSE TYPES TO EXTRACT:
{clause_types_list}

Respond with ONLY a JSON array of objects (no markdown, no explanation).
Each object must have this exact format:
{{
  "clause_type": "the clause type name",
  "found": true or false,
  "extracted_text": "exact word-for-word quote from contract" or null,
  "section_reference": "section number or paragraph reference" or null,
  "confidence": 0.0 to 1.0,
  "verification": "verified" or "not_applicable"
}}

IMPORTANT: If a clause type is NOT present, include it with found: false.
Do NOT fabricate clauses. Only extract text that literally appears in the contract.

CONTRACT TEXT:
{contract_text}\
"""

# ── CaseHOLD Precedent Ranking ─────────────────────────────────

CASEHOLD_SYSTEM_PROMPT = """\
You are Julia, a legal analysis assistant specializing in case law analysis.
Your task is to identify the correct holding of a cited case based on the
context in which it is cited.

CONSTRAINTS:
- Analyze the citing passage carefully to understand WHY the case was cited.
- Select the holding that best matches the legal principle being invoked.
- Provide brief reasoning for your selection.
- Never provide legal advice — this is analysis only.\
"""

CASEHOLD_PREDICT = """\
A court opinion cites a case. Based on the context of the citation, select which
of the 5 candidate holdings is the correct holding for the cited case.

CITING PASSAGE (the <HOLDING> marker shows where the holding should go):
{citing_prompt}

CANDIDATE HOLDINGS:
0: {holding_0}
1: {holding_1}
2: {holding_2}
3: {holding_3}
4: {holding_4}

Respond with ONLY a JSON object (no markdown, no explanation):
{{
  "predicted_idx": 0-4,
  "confidence": 0.0 to 1.0,
  "reasoning": "brief explanation of why this holding matches the citation context"
}}\
"""


# ── High-stakes clause types that get iterative verification ───

HIGH_STAKES_CLAUSE_TYPES = frozenset({
    "Indemnification",
    "Limitation Of Liability",
    "Cap On Liability",
    "Uncapped Liability",
    "Ip Ownership Assignment",
    "Joint Ip Ownership",
    "Irrevocable Or Perpetual License",
})


def build_cuad_single_prompt(clause_type: str, contract_text: str) -> str:
    """Build a single clause extraction prompt."""
    return CUAD_EXTRACT_SINGLE.format(
        clause_type=clause_type,
        contract_text=contract_text,
    )


def build_cuad_verify_prompt(
    clause_type: str,
    extracted_text: str,
    section_reference: str,
    contract_text: str,
) -> str:
    """Build a verification prompt for iterative refinement."""
    return CUAD_VERIFY_EXTRACTION.format(
        clause_type=clause_type,
        extracted_text=extracted_text,
        section_reference=section_reference or "not specified",
        contract_text=contract_text,
    )


def build_cuad_batch_prompt(clause_types: list[str], contract_text: str) -> str:
    """Build a batch extraction prompt for multiple clause types."""
    types_list = "\n".join(f"- {ct}" for ct in clause_types)
    return CUAD_EXTRACT_BATCH.format(
        clause_types_list=types_list,
        contract_text=contract_text,
    )


def build_casehold_prompt(
    citing_prompt: str,
    holdings: list[str],
) -> str:
    """Build a CaseHOLD prediction prompt."""
    return CASEHOLD_PREDICT.format(
        citing_prompt=citing_prompt,
        holding_0=holdings[0],
        holding_1=holdings[1],
        holding_2=holdings[2],
        holding_3=holdings[3],
        holding_4=holdings[4],
    )
