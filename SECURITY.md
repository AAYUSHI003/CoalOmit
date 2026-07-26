# Security Policy

## Supported Versions

We maintain the latest minor release of each open-source package (`cac-core`, `cac-cli`, `cac-action`). Older versions may receive security backports at our discretion, but we can't guarantee it, so if you're on an older release, please upgrade before filing a report — there's a good chance it's already fixed.

The `enterprise/` components (dashboard, hosted API, compliance exports, billing) follow whatever support terms are in your CarbonLens agreement.

## Reporting a Vulnerability

Please don't open a public GitHub issue for security problems. Instead, use one of these:

- GitHub Security Advisories (preferred): https://github.com/AAYUSHI003/carbon_lens/security/advisories/new
- Email: CarbonlensSecurity@gmail.com

A good report usually includes what's affected, how to reproduce it, and what the impact looks like — a proof-of-concept helps but isn't required. If you're not sure whether something counts as a security issue, send it anyway and we'll sort it out.

We'll acknowledge new reports within a few business days and follow up with an initial severity assessment shortly after. From there we'll keep you posted as we work through a fix, generally checking in every couple of weeks if it's taking a while. We ask that you give us a reasonable amount of time to patch things before disclosing publicly — coordinated disclosure keeps this useful for everyone, including your fellow users. If you'd like credit once it's fixed, we're happy to name you in the advisory or release notes.

## What's In Scope

- The open-source packages under `packages/`: `cac-core`, `cac-cli`, `cac-action`
- The GitHub Action itself
- `enterprise/` — the dashboard, hosted API, compliance exports, and billing, for customers with a support agreement

Not really in scope: vulnerabilities that live entirely in a third-party dependency (report those upstream, though a heads-up to us is still welcome), anything requiring an already-compromised machine or stolen credentials, or issues confined to the example notebooks in `examples/`.

## A Note on Local Data

`cac-core` and `cac-cli` are designed to run locally — model weights, activations, and benchmark output shouldn't leave your machine unless you've configured them to. If you find a path where that's not true (the grid-intensity lookups in `scripts/` are the most likely candidate, since they do reach out to the network), treat it as a security bug and report it, not just a functional one.

The hosted enterprise API is a different story — data handling there is governed by your organization's agreement, so check with your account contact for the specifics, or route security-specific concerns through the channels above.

## Dependencies

We pin dependency versions and run automated scanning to catch known CVEs early. Release artifacts for `cac-cli` and `cac-action` are built through CI from tagged commits, so if you're deploying in a sensitive environment, it's worth verifying checksums or signatures before you do.

## Thanks

Security reports from the community have made this project better, and we appreciate the time it takes to write a good one.