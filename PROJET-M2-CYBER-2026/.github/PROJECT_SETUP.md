# Instructions to Create GitHub Project Board Manually

Since the automation token lacks required scopes, follow these steps:

## 1. Create Project Board
1. Go to: https://github.com/yugmerabtene/PROJET-M2-CYBER-2026
2. Click **Projects** tab → **New project**
3. Select **Board** template (Scrum/Kanban)
4. Name: `DevinciWatch Scrum Board`
5. Description: `MVP development - 5 Sprints, 90 SP, 9 team members`

## 2. Configure Columns (Status)
Create these columns:
- **Backlog** (To Do)
- **Sprint Ready** (Ready)
- **In Progress** (Doing)
- **In Review** (Review)
- **Done** (Done)

## 3. Add Custom Fields
In Project Settings → Fields, add:
- **Epic** (Single select): EPIC-01 to EPIC-08
- **Story Points** (Number): Fibonacci (1,2,3,5,8,13)
- **Sprint** (Single select): Sprint 1 to Sprint 5
- **Owner** (Single select): Ada Lovelace, Grace Hopper, Alan Turing, Barbara Liskov, Ken Thompson, Tim Berners-Lee, Margaret Hamilton, Linus Torvalds, Radia Perlman

## 4. Add Issues to Board
Already created issues (1-5) will appear. Add them to board:
- Issue #1: Epic=EPIC-01, SP=5, Sprint=1, Owner=Barbara Liskov
- Issue #2: Epic=EPIC-02, SP=8, Sprint=1, Owner=Ken Thompson
- Issue #3: Epic=EPIC-03, SP=13, Sprint=2, Owner=Alan Turing
- Issue #4: Epic=EPIC-04, SP=13, Sprint=2, Owner=Radia Perlman
- Issue #5: Epic=EPIC-02, SP=0, Sprint=1, Owner=Alan Turing

## 5. Create Remaining Issues (Optional)
Use the GitHub CLI or web interface to create issues for:
- US-01.2, US-01.3 (Socle Applicatif)
- US-02.2, US-02.3 (Collecte & Endpoint)
- US-03.2, US-03.3 (Découverte Actifs)
- US-04.2, US-04.3 (Détection & Alertes)
- US-05.1, US-05.2, US-05.3 (Corrélation)
- US-06.1, US-06.2, US-06.3 (Interface Web)
- US-07.1, US-07.2, US-07.3 (Reporting & Exports)
- US-08.1, US-08.2, US-08.3 (Lab Docker)

Total: 24 User Stories, 90 Story Points

## 6. Verify Board
- URL: https://github.com/users/yugmerabtene/projects/
- Check all 5 Sprints configured
- Check 90 SP total in Sprint views
- Check RACI matrix matches `tasks/team-assignments.md`
