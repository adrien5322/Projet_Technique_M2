---
name: Bug Report
about: Report a bug found during MVP development
title: '[BUG] '
labels: 'bug'
assignees: []

body:
  - type: dropdown
    id: severity
    attributes:
      label: 'Severity'
      options:
        - 'Critical (blocks MVP)'
        - 'High (major feature broken)'
        - 'Medium (partial functionality issue)'
        - 'Low (cosmetic/minor)'
      required: true

  - type: dropdown
    id: component
    attributes:
      label: 'Component (from Architecture §3)'
      options:
        - 'Backend API (serveur-soc)'
        - 'Backend Workers (Celery)'
        - 'Frontend (Dashboard)'
        - 'Database (PostgreSQL)'
        - 'Cache (Redis)'
        - 'Docker/Lab (serveur-endpoint, serveur-attacker)'
        - 'Security (Auth, Roles, Audit)'
      required: true

  - type: input
    id: sprint
    attributes:
      label: 'Sprint (from 07_gestion_de_projet §11)'
      placeholder: 'e.g., Sprint 3'
      value: ''

  - type: textarea
    id: description
    attributes:
      label: 'Bug Description'
      value: 'Describe the bug clearly...'
      required: true

  - type: textarea
    id: steps
    attributes:
      label: 'Steps to Reproduce'
      value: |
        1. 
        2. 
        3. 
      required: true

  - type: textarea
    id: expected
    attributes:
      label: 'Expected Behavior'
      value: 'What should happen?'
      required: true

  - type: textarea
    id: actual
    attributes:
      label: 'Actual Behavior'
      value: 'What actually happens?'
      required: true

  - type: input
    id: owner
    attributes:
      label: 'Assign to (from 07_gestion_de_projet §4)'
      placeholder: 'e.g., Barbara Liskov, Tim Berners-Lee'
      value: ''

  - type: markdown
    attributes:
      value: |
        ## Notes
        - Link to [Scrum Board](documents/07_gestion_de_projet/rendu_principal.md)
        - Critical bugs should be fixed within the same sprint
        - Add proof: screenshot, log, or export
