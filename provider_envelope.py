"""Shared strict provider envelope extraction; raw evidence is never modified."""
from runtime_contract import Reject, parse

def verdict_text(content):
    """Ignore provider reasoning envelopes; verdict bytes come only from text."""
    if not isinstance(content, list): raise Reject('unexpected provider content')
    texts = []
    for block in content:
        if not isinstance(block, dict): raise Reject('unexpected provider content')
        kind = block.get('type')
        if kind == 'text':
            if not isinstance(block.get('text'), str): raise Reject('invalid provider text')
            texts.append(block['text'])
        elif kind in ('thinking','redacted_thinking'):
            field='thinking' if kind=='thinking' else 'data'
            if not isinstance(block.get(field),str): raise Reject('invalid provider reasoning envelope')
            if 'signature' in block and not isinstance(block['signature'],str): raise Reject('invalid provider reasoning signature')
        else:
            raise Reject('unexpected provider content')
    if not texts or not ''.join(texts).strip(): raise Reject('missing provider text')
    return ''.join(texts)


def provider_response(raw, expected_model=None):
    response=parse(raw)
    if not isinstance(response,dict): raise Reject("unexpected provider response")
    if response.get("stop_reason")!="end_turn": raise Reject("truncated or incomplete output")
    model=response.get("model")
    if not isinstance(model,str): raise Reject("invalid provider model")
    if expected_model is not None:
        import re
        if model!=expected_model and not re.fullmatch(re.escape(expected_model)+r"-\d{8}",model): raise Reject("unexpected provider model")
    return response, verdict_text(response.get("content")).encode("utf-8")
