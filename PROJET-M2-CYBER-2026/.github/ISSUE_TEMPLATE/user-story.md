---
name: User Story
about: Create a new User Story (Epic/Feature/Story)
title: '[US-XX.X] '
labels: 'user-story'
assignees: []

body:
  - type: checkboxes
    attributes:
      label: 'Epic (link to 07_gestion_de_projet §8-9)'
      options:
        - label: 'EPIC-01 - Socle applicatif et sécurité'
          required: true
        - label: 'EPIC-02 - Collecte endpoint et télémétrie'
        - label: 'EPIC-03 - Découverte réseau et actifs'
        - label: 'EPIC-04 - Détection, alertes et audit'
        - label: 'EPIC-05 - Corrélation et enrichissement analyste'
        - label: 'EPIC-06 - Interface web et visualisation'
        - label: 'EPIC-07 - Reporting, exports et preuves'
        - label: 'EPIC-08 - Lab Docker, démonstration et documentation'

  - type: input
    id: story-id
    attributes:
      label: 'Story ID (e.g., US-01.1)'
      placeholder: 'US-XX.X'
      value: ''

  - type: textarea
    id: user-story
    attributes:
      label: 'User Story (As a..., I want..., So that...)'
      value: 'En tant que [role], je veux [action] afin de [goal].'
      required: true

  - type: dropdown
    id: story-points
    attributes:
      label: 'Story Points (Fibonacci)'
      options:
        - '1'
        - '2'
        - '3'
        - '5'
        - '8'
        - '13'
      required: true

  - type: dropdown
    id: sprint
    attributes:
      label: 'Sprint cible (from 07_gestion_de_projet §11)'
      options:
        - 'Sprint 1 (Socle + Docker initial)'
        - 'Sprint 2 (Ingestion + Actifs)'
        - 'Sprint 3 (Détection + Alertes)'
        - 'Sprint 4 (Corrélation + Interface)'
        - 'Sprint 5 (Stabilisation + Preuves)'
      required: true

  - type: dropdown
    id: owner
    attributes:
      label: 'Owner (from 07_gestion_de_projet §4)'
      options:
        - 'Barbara Liskov (Backend 1)'
        - 'Ken Thompson (Backend 2)'
        - 'Tim Berners-Lee (Frontend)'
        - 'Margaret Hamilton (QA/Tests)'
        - 'Linus Torvalds (DevOps)'
        - 'Radia Perlman (Cybersécurité)'
      required: true

  - type: textarea
    id: tasks
    attributes:
      label: 'Technical Tasks (checklist)'
      value: |
        - [ ] Task 1
        - [ ] Task 2
        - [ ] Task 3

  - type: textarea
    id: acceptance-criteria
    attributes:
      label: 'Acceptance Criteria (Definition of Done)'
      value: |
        - [ ] Criterion 1
        - [ ] Criterion 2
        - [ ] Preuve de validation générée

  - type: input
    id: cross-refs
    attributes:
      label: 'Cross-references (Architecture §5, Cahier des charges §6)'
      placeholder: 'e.g., Architecture §5.1, Cahier §6.2'
      value: ''

  - type: markdown
    attributes:
      value: |
        ## Notes
        - Link to [Gestion de projet §8-10](documents/07_gestion_de_projet/rendu_principal.md)
        - Use Fibonacci: 1,2,3,5,8,13
        - Definition of Ready: clear objective, identified user, acceptance criteria written
        - Definition of Done: implemented, tested, persisted, documented, proof generated
