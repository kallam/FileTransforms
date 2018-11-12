from typing import List, Dict
import os
import json
from difflib import get_close_matches


def normalize_header(header):
    while '  ' in header:
        header = header.replace('  ', ' ')

    return header.strip().upper()


def load_headers(headers_filename):
    if not os.path.exists(headers_filename):
        return None

    with open(headers_filename) as headers_file:
        return json.load(headers_file)


def generate_header_lookup_dict(tokens_dict):
    header_map = {}

    for k in tokens_dict:
        norm_k = normalize_header(k)
        if isinstance(tokens_dict[k], list):
            for val in tokens_dict[k]:
                v = normalize_header(val)
                if v in header_map and header_map[v] == norm_k:
                    print('{} - {} already exists in file'.format(k, val))
                header_map[v] = norm_k
        else:
            header_map[normalize_header(tokens_dict[k])] = norm_k

    return header_map


def check_potential_headers_transformation(raw_headers, tokens_dict):
    header_map = generate_header_lookup_dict(tokens_dict)
    found = []

    for header in raw_headers:
        if not try_header_variations(header, header_map, [])[0]:
            found.append("'{}': Tokens.{},".format(header, 'SKIP'))


def try_header_variations(header: str, header_map: Dict[str, str], all_headers: List[str],
                          header_ratio_min: float = 1.0) -> (bool, str):
    if not header_map:
        return False, header

    header = normalize_header(header)

    if header in header_map:
        return True, header_map[header]

    variations = [header]

    if '\'S' in header:
        header = header.replace('\'S', '')
        variations.append(header)

    for variant, replacement in (
            ('GUARANTOR', 'RESPONSIBLE'), ('GUAR ', 'RESPONSIBLE '), ('RESPONSIBLE PARTY', 'RESPONSIBLE'),
            ('DATE OF BIRTH', 'DOB')):
        if variant in header:
            s = header.replace(variant, replacement)
            if s not in variations:
                variations.append(s)

    best_k = None
    best_ratio = 0.0

    for var_header in variations:
        if ' ' in var_header:
            if var_header.replace(' ', '_') in all_headers:
                return True, var_header.replace(' ', '_')

        if var_header in header_map.keys():
            ret = header_map[var_header]
            if ret[:6] != 'OTHER_' and ret[:6] != 'NOTES_' and ret[:8] != 'COMMENTS_':
                del header_map[var_header]
            return True, ret

        for k in filter(lambda _k: _k in var_header, header_map.keys()):
            ratio = len(k) / 1.0 / len(var_header)
            if ratio > best_ratio:
                best_ratio = ratio
                best_k = k

    if best_ratio > header_ratio_min:
        ret = header_map[best_k]
        if ret[:6] != 'OTHER_' and ret[:6] != 'NOTES_' and ret[:8] != 'COMMENTS_':
            del header_map[best_k]

        return True, ret

    # Check for missing/added spaces
    for var_header in variations:
        matches = get_close_matches(var_header, header_map.keys(), 1, 0.9)
        if len(matches) > 0:
            ret = header_map[matches[0]]
            del header_map[matches[0]]
            return True, ret

    return False, header


def enumerate_headers(headers, tokens, start_idx=1):
    token_counts = {}
    for t in tokens:
        token_counts[t] = start_idx

    for i, header in enumerate(headers):
        if header in tokens:
            headers[i] = header + str(token_counts[header])
            token_counts[header] += 1

    return headers
