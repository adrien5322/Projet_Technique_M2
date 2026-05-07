---
name: Technical Task
about: Create a technical task linked to a User Story
title: '[TASK] '
labels: 'task'
assignees: []

body:
  - type: input
    id: task-id
    attributes:
      label: 'Task ID (e.g., T-01.1.1)'
      placeholder: 'T-XX.X.Y'
      value: ''

  - type: input
    id: user-story
    attributes:
      label: 'Parent User Story (from 07_gestion_de_projet §10)'
      placeholder: 'e.g., US-01.1'
      value: ''
      required: true

  - type: dropdown
    id: component
    attributes:
      label: 'Component (from Architecture §3)'
      options:
        - 'Backend - FastAPI route'
        - 'Backend - SQLAlchemy model'
        - 'Backend - Celery worker'
        - 'Backend - Redis cache'
        - 'Frontend - UI component'
        - 'Frontend - Navigation'
        - 'DevOps - Docker'
        - 'Security - Auth/ Roles'
        - 'QA - Test case'
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
    id: description
    attributes:
      label: 'Task Description'
      value: 'Describe the technical task...'
      required: true

  - type: input
    id: estimate
    attributes:
      label: 'Estimate (hours)'
      placeholder: 'e.g., 2h, 4h, 1d'
      value: ''

  - type: dropdown
    id: status
    attributes:
      label: 'Status'
      options:
        - 'To Do'
        - 'In Progress'
        - 'Done'
      required: true

  - type: input
    id: cross-refs
    attributes:
      label: 'Cross-references (Architecture, Cahier des charges)'
      placeholder: 'e.g., Architecture §5.1'
      value: ''

  - type: markdown
    attributes:
      value: |
        ## Notes
        - Link task to parent User Story using "Closes #XX" in PR
        - Update Definition of Done in 07_gestion_de_projet when task completes
        - Add proof: commit hash, test result, or screenshot
