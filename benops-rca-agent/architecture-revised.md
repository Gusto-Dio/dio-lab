# BenOps RCA Agent — Arquitetura Revisada

**Data:** 2026-05-30
**Autor:** Diogenes Ribeiro (BizTech RPA)
**Status:** Aprovada para implementação
**Evento:** Benefits Hackathon — Junho 2026

---

## Visão Geral

Agente Python autônomo que detecta jobs Faulted no UiPath Orchestrator, realiza uma investigação de causa raiz em 3 fases via Claude API, e entrega um ticket Jira pré-diagnosticado + alerta Slack em menos de 60 segundos.

---

## Decisão Arquitetural Principal

O `uip` CLI (UiPath CLI) está instalado no ambiente e já sabe consultar o Orchestrator nativamente via JSON estruturado. O design original previa wrappers Python para a API REST do Orchestrator — desnecessário. O agente usa `subprocess` para chamar o `uip` CLI diretamente, reduzindo ~40% do código necessário.

---

## Estrutura de Arquivos

```
benops-rca-agent/
├── agent/
│   ├── main.py                  # entry point — loop de polling
│   ├── failure_listener.py      # detecta jobs Faulted via uip CLI
│   ├── context_collector.py     # coleta dados em paralelo (uip + GitHub)
│   ├── ai_analyst.py            # 3 fases de investigação — Claude API
│   ├── priority_checker.py      # verifica prioridade via Orchestrator Asset
│   ├── jira_creator.py          # cria ticket Jira com RCA estruturado
│   └── slack_notifier.py        # posta alerta no Slack
├── prompts/
│   ├── system_prompt.md         # conhecimento UiPath — CACHED na Claude API
│   ├── triage_prompt.md         # Fase 1
│   ├── investigate_prompt.md    # Fase 2
│   └── rca_prompt.md            # Fase 3
├── config/
│   └── settings.py              # env vars e configurações
├── requirements.txt
└── README.md
```

---

## Componentes

### 1. Failure Listener

Faz polling a cada 60 segundos. Usa `uip` CLI para detectar jobs Faulted sem precisar de wrapper REST.

```bash
uip or jobs list --state Faulted --folder-key <key> --output json
```

Mantém um set de job keys já processados para evitar duplicatas.

---

### 2. Context Collector

Coleta dados em paralelo usando `concurrent.futures`. Mistura de `uip` CLI (Orchestrator) e GitHub REST API (XAML + PRs).

| Dado | Fonte | Método |
|---|---|---|
| Job details | Orchestrator | `uip or jobs get <key> --output json` |
| Execution logs | Orchestrator | `uip or jobs logs <key> --output json` |
| State history | Orchestrator | `uip or jobs history <key> --output json` |
| Execution traces | Orchestrator | `uip traces spans get --job-key <key> --output json` |
| XAML source | GitHub API | `GET /repos/{org}/{repo}/contents/{path}` |
| PR history | GitHub API | `GET /repos/{org}/{repo}/pulls?state=closed` |

---

### 3. AI Analyst — 3 Fases

Núcleo do agente. Usa Claude API com Prompt Caching e Tool Use.

#### System Prompt (CACHED — nunca muda)

Inclui conhecimento extraído das UiPath skills instaladas:
- Playbooks de falha do `uipath-troubleshoot` (Orchestrator, UI Automation, System Activities)
- Padrões e armadilhas XAML do `uipath-rpa`
- Taxonomia de falhas BenOps (portal_change, data_quality, business_rule, network_timeout, library_incompatibility, unknown)
- Schema de output estruturado

#### Fase 1 — Triage (sem tools, ~5s)

**Entrada:** job metadata + mensagem de erro inicial do Orchestrator
**Saída:** domínio classificado + hipóteses rankeadas por confiança

```json
{
  "domain": "ui_automation | system_activities | runtime_exception | orchestrator",
  "hypotheses": [
    {"type": "portal_change", "confidence": "high", "evidence_needed": ["xaml_file", "pr_history"]},
    {"type": "network_timeout", "confidence": "medium", "evidence_needed": ["job_traces"]}
  ]
}
```

#### Fase 2 — Investigação (tool use loop, ~20-30s)

Claude chama tools conforme as hipóteses da Fase 1. Só busca o que precisa.

| Tool | Descrição | Mapeamento |
|---|---|---|
| `get_job_traces(job_key)` | Execution traces | `uip traces spans get` |
| `get_xaml_file(process, filename)` | Código XAML (CACHED por processo) | GitHub API |
| `get_pr_history(process, n)` | Últimos N PRs merged | GitHub API |
| `get_queue_items(queue_key)` | Items failed/successful para comparação | `uip resource queue-items list` |
| `get_similar_tickets(process, error)` | Tickets passados similares | Jira REST API |

#### Fase 3 — RCA (submit_rca tool, ~5s)

Claude encerra o loop chamando `submit_rca` com o output estruturado.

```json
{
  "failure_type": "portal_change",
  "root_cause": "Selector mismatch no step EnterMemberInformation — carrier atualizou portal",
  "affected_file": "EnterMemberInformation.xaml",
  "line_number": 142,
  "suggested_fix": "Atualizar aaname selector — novo valor: 'Submit Enrollment'",
  "severity": "high",
  "affected_transactions": ["500R7000009XABC"],
  "confidence": "high"
}
```

#### Estratégia de Prompt Caching

| Conteúdo | Cache | Invalida quando |
|---|---|---|
| System prompt + playbooks UiPath | Permanente | Nunca (manualmente) |
| XAML source files | Por processo | Novo PR merged no processo |
| Job logs + metadata | Sem cache | Sempre fresh |

---

### 4. Priority Checker

Consulta um Orchestrator Asset configurável para determinar se o processo é high-priority. Não requer mudança de código para atualizar a lista.

```bash
uip or assets get "RCA_Priority_Processes" --folder-key <key> --output json
```

**Comportamento por prioridade:**

| Prioridade | Ação |
|---|---|
| High | Cria ticket Jira + posta no #benops-rpa-alerts |
| Standard | Posta apenas no #benops-rpa-dev |

---

### 5. Jira Creator

Cria ticket via Jira REST API com o RCA estruturado.

**Formato do ticket:**
```
Título:   [RCA-AUTO] {ProcessName} — {failure_type} — {YYYY-MM-DD}
Labels:   rca-auto, {failure_type}, {severity}
Links:    Orchestrator Job | GitHub XAML file
```

---

### 6. Slack Notifier

Posta mensagem formatada com blocos Slack (Block Kit).

**Canal high-priority:** `#benops-rpa-alerts`
**Canal standard:** `#benops-rpa-dev`

---

## Fluxo Completo

```
Orchestrator (job Faulted)
        │
        ▼ polling 60s
Failure Listener  →  job key já processado? → ignora
        │
        ▼ novo job
Context Collector  ←──────────────────────────┐
  ├── uip or jobs get          (paralelo)      │
  ├── uip or jobs logs         (paralelo)      │
  ├── uip or jobs history      (paralelo)      │
  └── uip traces spans get     (paralelo)      │
        │                                      │
        ▼                                      │
AI Analyst                                     │
  ├── Fase 1: Triage                           │
  │     └── classifica + gera hipóteses        │
  ├── Fase 2: Investigação (tool use)          │
  │     ├── get_xaml_file ──────────────────── │ GitHub API
  │     ├── get_pr_history ────────────────────│ GitHub API
  │     ├── get_job_traces ────────────────────│ uip CLI
  │     └── get_similar_tickets ───────────────│ Jira API
  └── Fase 3: RCA estruturado
        │
        ▼
Priority Checker  ←── uip or assets get "RCA_Priority_Processes"
        │
        ├── HIGH ──→ Jira Creator + Slack (#benops-rpa-alerts)
        └── STD  ──→ Slack (#benops-rpa-dev)
```

---

## Dependências e Tokens

| Dependência | Status | Método de acesso | Usado por |
|---|---|---|---|
| `uip` CLI (UiPath CLI) | Já instalado | subprocess | Failure Listener, Context Collector, Priority Checker |
| Anthropic Claude API | **Novo** | `ANTHROPIC_API_KEY` | AI Analyst |
| GitHub REST API | Já em uso | `GITHUB_TOKEN` | Context Collector (XAML + PRs) |
| Jira REST API | Já em uso | `JIRA_TOKEN` + `JIRA_BASE_URL` | AI Analyst (tool), Jira Creator |
| Slack API | Já em uso | `SLACK_TOKEN` | Slack Notifier |

---

## Requirements

### Runtime

| Requisito | PoC (Mac) | Produção (Linux/Windows) |
|---|---|---|
| Python | 3.11+ | 3.11+ |
| `uip` CLI | Instalado via npm | Instalar via `npm -g install @uipath/cli` |
| Node.js | 18+ (dependência do uip) | 18+ |
| Memória | ~256 MB | ~256 MB |
| CPU | 1 core | 1 core |
| Rede | Acesso à internet (Orchestrator Cloud, GitHub, Jira, Slack, Anthropic) | Idem |

### Variáveis de Ambiente

```bash
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...
JIRA_TOKEN=...
JIRA_BASE_URL=https://gusto.atlassian.net
JIRA_PROJECT_KEY=BT
SLACK_TOKEN=xoxb-...
SLACK_ALERT_CHANNEL=#benops-rpa-alerts
SLACK_DEV_CHANNEL=#benops-rpa-dev
ORCHESTRATOR_FOLDER_KEY=...       # folder key do Orchestrator
ORCHESTRATOR_REPO=biztech-uipath-rpa   # repo GitHub dos processos
ORCHESTRATOR_ORG=Gusto                  # org GitHub
POLL_INTERVAL_SECONDS=60
```

### requirements.txt

```
anthropic>=0.30.0
requests>=2.31.0
python-dotenv>=1.0.0
```

> **Nota:** Orchestrator, Jira, Slack e GitHub são acessados via `uip` CLI ou `requests` diretamente — sem SDKs adicionais.

---

## Compatibilidade Cross-Platform

| Aspecto | Mac (PoC) | Linux (produção) | Windows (produção) |
|---|---|---|---|
| Python | ✅ homebrew / pyenv | ✅ apt / pyenv | ✅ python.org |
| `uip` CLI | ✅ npm global | ✅ npm global | ✅ npm global |
| subprocess calls | ✅ | ✅ | ✅ (mesmo código) |
| Env vars | `.env` / export | `.env` / systemd | `.env` / Task Scheduler |
| Execução contínua | Terminal / launchd | systemd service | Windows Service / Task Scheduler |

O código Python não tem dependências de plataforma — o único ponto de atenção é o path do `uip` CLI, que deve estar no `PATH` do sistema.

---

## Fora do Escopo (Hackathon v1)

- Auto-aplicação do fix (agente diagnostica, humano corrige)
- Dashboard UI (terminal + Jira + Slack é suficiente para v1)
- Webhook trigger (polling é suficiente para demo; webhook é melhoria pós-hackathon)
- Auto-documentação de processos (iniciativa separada)
- Retry automático de jobs (requer aprovação humana)
