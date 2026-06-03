# BenOps RPA — Runbooks

**Repositório:** biztech-uipath-rpa  
**Time:** BenOps RPA — Gusto BizTech  
**Última atualização:** 2026-06-03

Todos os runbooks abaixo são baseados em incidentes e tarefas reais vividos pelo time.

---

## 1. Buildkite falhou na PR

**Quando usar:** Pipeline falha após `git push` em qualquer PR do repo.

Existem três padrões distintos — identifique pelo erro antes de agir.

### Padrão A — Versão não bumped

**Erro:**
```
process can't be upgraded from version X.X.X to X.X.X
```

**Fix:**
1. Abrir `{ProcessFolder}/project.json`
2. Incrementar `projectVersion` em um patch: ex. `1.3.6` → `1.3.7`
3. Stagear e commitar apenas o `project.json`:
```powershell
git add "Processes/.../project.json"
git commit -m "[BT-XXXXX] Bump {ProcessName} version X.X.X -> X.X.Y"
git push
```

### Padrão B — Branch atrás do develop (diff sujo)

**Sintoma:** Buildkite roda `check_dependency.sh` em processos que você não tocou.

**Diagnóstico:**
```powershell
git fetch origin develop
git diff origin/develop..HEAD --name-only
```
Se aparecerem arquivos fora da pasta do seu ticket, o branch está atrás.

**Fix:**
```powershell
git merge origin/develop --no-edit
git diff origin/develop..HEAD --name-only  # confirmar que só seus arquivos aparecem
git push
```

### Padrão C — check_dependency.sh falha em processo fora do escopo

**Erro:**
```
check_dependency.sh Processes/.../SomeOtherProcess
Error: dependency X version Y.Y.Y does not meet requirement
```

**Causa:** Padrão B — o processo alheio apareceu no diff. Fix: mesmo que o Padrão B acima.

### Checklist pré-PR (previne os três padrões)

```powershell
git fetch origin develop
git diff origin/develop..HEAD --name-only   # deve mostrar só os arquivos do ticket
# Se aparecer algo fora do escopo:
git merge origin/develop --no-edit
git diff origin/develop..HEAD --name-only   # confirmar novamente
```

---

## 2. Bot falhando em produção — triage inicial

**Quando usar:** Job falhou no Orchestrator com SystemException ou BusinessRuleException.

### Passo 1 — Identificar o tipo de exceção no log

- **BusinessRuleException:** dado inválido ou condição de negócio não atendida. Verificar os dados do item na fila (SF ID, datas, planos). Não é bug de código.
- **SelectorNotFoundException / UiPath.Core.SelectorNotFoundException:** elemento da UI não encontrado. Ir para Passo 2.
- **NullReferenceException / KeyNotFoundException:** variável ou chave de Config/dicionário vazia. Verificar Config.json e Assets no Orchestrator.
- **System.Exception genérica:** ler a mensagem completa no log — geralmente tem o arquivo e linha.

### Passo 2 — Verificar se é problema de navegação/selector

- Abrir o screenshot de erro (bucket S3 ou pasta `ExceptionScreenshots`)
- Verificar se o portal estava em estado inesperado (loading, modal aberto, sessão expirada)
- Se o elemento sumiu do portal: selector provavelmente precisa de atualização

### Passo 3 — Verificar InteractionMode

```powershell
Select-String -Path "Processes\...\**\*.xaml" -Pattern "DebuggerApi" -Recurse
```
Se retornar resultados: o processo tem `InteractionMode="DebuggerApi"` que só funciona no debugger do Studio. Ver Runbook 3.

### Passo 4 — Verificar infra da VM

- Python não encontrado: checar se `C:\Windows\System32\python.cmd` existe
- Screenshot falhando: checar se `C:\Program Files\PowerShell\7\pwsh.exe` existe
- Job travado em Running: matar o job no Orchestrator, reiniciar o Robot se necessário

### Passo 5 — Reproduzir em Dev antes de corrigir

- Nunca fazer fix direto em produção
- Criar item de teste na fila de Dev/Staging com os mesmos dados do item que falhou
- Confirmar que o problema se reproduz antes de codificar o fix

---

## 3. DebuggerApi em processo migrado

**Quando usar:** Bot falha em produção com clicks que não respondem, ou você está revisando um processo recém-migrado do Legacy para Windows.

**Causa:** Durante a migração Legacy → Windows, o Studio às vezes define `InteractionMode="DebuggerApi"` nos activities de click. Esse modo só funciona conectado ao Studio em modo debug — em produção (Robot), os clicks são ignorados silenciosamente.

### Diagnóstico

```powershell
Select-String -Path "Processes\...\**\*.xaml" -Pattern "DebuggerApi" -Recurse
```

### Fix

Substituir todas as ocorrências por `Simulate` em cada arquivo afetado:

- No VS Code: Ctrl+Shift+H → buscar `InteractionMode="DebuggerApi"` → substituir por `InteractionMode="Simulate"` com escopo nos arquivos do processo
- Ou editar diretamente cada `.xaml` identificado

### Validação pós-fix

```powershell
# Confirmar que não sobrou nenhuma ocorrência
Select-String -Path "Processes\...\**\*.xaml" -Pattern "DebuggerApi" -Recurse
# Resultado esperado: vazio
```

---

## 4. Navigation flapping — RetryScope + NCheckState

**Quando usar:** Bot falha intermitentemente em clicks de navegação — o elemento existe mas o click não surte efeito, ou o portal ainda está carregando quando o click é executado.

**Padrão a aplicar:** Envolver o `NClick` problemático com `RetryScope` + `NCheckState`.

### Estrutura XAML

```xml
<ui:RetryScope DisplayName="Retry - Click 'ElementName'" NumberOfRetries="5" RetryInterval="00:00:03">
  <ui:RetryScope.ActivityBody>
    <ActivityAction>
      <Sequence DisplayName="Action">
        <Assign DisplayName="Reset elementFound">
          <Assign.To><OutArgument x:TypeArguments="x:Boolean">[elementFound]</OutArgument></Assign.To>
          <Assign.Value><InArgument x:TypeArguments="x:Boolean">[False]</InArgument></Assign.Value>
        </Assign>
        <uix:NCheckState DisplayName="Check 'ElementName'" Timeout="15" Version="V4">
          <uix:NCheckState.IfExists>
            <Sequence DisplayName="Target appears">
              <Assign DisplayName="Set elementFound = True">
                <Assign.To><OutArgument x:TypeArguments="x:Boolean">[elementFound]</OutArgument></Assign.To>
                <Assign.Value><InArgument x:TypeArguments="x:Boolean">[True]</InArgument></Assign.Value>
              </Assign>
              <uix:NClick ... InteractionMode="Simulate">
                <!-- target original do NClick -->
              </uix:NClick>
            </Sequence>
          </uix:NCheckState.IfExists>
          <uix:NCheckState.IfNotExists>
            <Sequence DisplayName="Target does not appear" />
          </uix:NCheckState.IfNotExists>
          <uix:NCheckState.Target>
            <!-- mesmo target do NClick -->
          </uix:NCheckState.Target>
        </uix:NCheckState>
      </Sequence>
    </ActivityAction>
  </ui:RetryScope.ActivityBody>
  <ui:RetryScope.Condition>
    <ActivityFunc x:TypeArguments="x:Boolean" />
  </ui:RetryScope.Condition>
</ui:RetryScope>
```

### Parâmetros

| Parâmetro | Valor | Motivo |
|---|---|---|
| `NumberOfRetries` | 5 | Cobre lentidão de rede sem loop infinito |
| `RetryInterval` | `00:00:03` | 3s entre tentativas |
| `NCheckState.Timeout` | 15 | 15s para o elemento aparecer |
| `RetryScope.Condition` | `ActivityFunc` vazio | Para quando não há exceção (sucesso) |

### Variável necessária

Declarar `elementFound` como `Boolean` com default `False` no escopo do workflow.

---

## 5. Legacy → Windows migration

**Quando usar:** Ticket de migração de um processo do framework Legacy para Windows Modern.

### Checklist completo

**1. Criar branch**
```
BT-XXXXX-CarrierName-ProcessType-windows-migration
```

**2. Atualizar project.json**
- `targetFramework`: `"Windows"`
- `expressionLanguage`: `"VisualBasic"` (manter)
- Atualizar todas as dependências para versões compatíveis com Windows
- Bumpar `projectVersion`

**3. Revisar todos os .xaml do processo**
- Substituir activities Legacy por equivalentes Modern (ex: `Click` → `NClick`, `TypeInto` → `NTypeInto`)
- Remover namespaces Legacy dos headers XAML
- Adicionar namespaces Modern onde necessário
- Verificar e corrigir todos os selectors

**4. Verificar InteractionMode**
```powershell
Select-String -Path "Processes\...\**\*.xaml" -Pattern "DebuggerApi" -Recurse
```
Substituir tudo por `Simulate`. Ver Runbook 3.

**5. Verificar navigation flapping**
Identificar NClicks de navegação crítica e aplicar padrão RetryScope + NCheckState. Ver Runbook 4.

**6. Validar**
```powershell
uip rpa get-errors --project-dir "C:\...\ProcessFolder" --output json
uip rpa build "C:\...\ProcessFolder" --output json
```
Resolver todos os erros antes de commitar.

**7. Testar em Orchestrator (Dev)**
- Mínimo 2-3 transações
- Documentar Transaction IDs

**8. PR**
- Diff limpo (só arquivos do processo migrado)
- Versão bumped
- Transaction IDs na descrição

---

## 6. Library version bump

**Quando usar:** Uma correção ou melhoria foi feita em uma library compartilhada (ex: `Gusto_Benefits`, `Gusto_Modern_Generic`) e os processos dependentes precisam ser atualizados.

### Identificar processos dependentes

```powershell
Select-String -Path "Processes\**\project.json" -Pattern "LibraryName" -Recurse
```

### Atualizar dependência no project.json

```json
"LibraryName": "1.550.8"
```
- Versão exata (sem colchetes): sempre usa essa versão
- Versão com colchetes `[1.550.8]`: usa exatamente essa, não resolve automaticamente
- Versão com intervalo `[1.550.0,)`: usa essa ou superior

### Quando bumpar patch vs minor

| Situação | Incremento |
|---|---|
| Bug fix em activity existente | Patch: `1.550.7` → `1.550.8` |
| Nova activity adicionada | Minor: `1.550.x` → `1.551.0` |
| Breaking change / refactor | Major: `1.x.x` → `2.0.0` |

### Validar após bump

```powershell
uip rpa get-errors --project-dir "C:\...\ProcessFolder" --output json
uip rpa build "C:\...\ProcessFolder" --output json
```

### Bumpar versão do processo também

Sempre que atualizar uma dependência, bumpar o `projectVersion` do processo afetado. Ver Runbook 1 Padrão A.

---

## 7. Fluxo completo de PR — do commit ao merge

**Quando usar:** Referência para todo ticket antes de abrir PR.

### Passo 1 — Stagear apenas arquivos do ticket

```powershell
git add "Processes/.../File1.xaml"
git add "Processes/.../project.json"
git status --short   # confirmar: só arquivos do ticket com "M " (staged)
```

### Passo 2 — Verificar diff

```powershell
git fetch origin develop
git diff origin/develop..HEAD --name-only
# Se aparecer arquivo fora do escopo: git merge origin/develop --no-edit
```

### Passo 3 — Commitar

```
[BT-XXXXX] CarrierName ProcessName — descrição concisa

- Mudança específica 1
- Mudança específica 2
```

### Passo 4 — Push e abrir PR

Título: `[BT-XXXXX] CarrierName ProcessName — Fix/Feature Description`

Body obrigatório:
- Summary (2-3 bullets)
- Changes (arquivo por arquivo)
- Test Plan
- Transactions Tested (Transaction ID + resultado)

### Passo 5 — Após Buildkite passar

- Comentar no ticket Jira com link da PR
- Notificar no canal do time no Slack (`#benops-rpa` ou canal equivalente) mencionando os reviewers

### Passo 6 — Após merge

- Confirmar que o pipeline de deploy passou
- Verificar no Orchestrator que o package foi publicado na versão correta
- Fechar ou transicionar o ticket no Jira

---

## 8. Publicar library no Orchestrator

**Quando usar:** Uma nova versão de library foi buildada e precisa ser publicada no Orchestrator para que os processos dependentes possam usá-la.

### Buildar o package

```powershell
uip rpa pack --project-dir "C:\...\LibraryFolder" --output-dir "C:\...\LibraryFolder\output" --description "v1.550.8 - fix description"
```

### Publicar via PowerShell (obrigatório — não usar Python)

> Cloudflare bloqueia chamadas HTTP feitas por Python/urllib. Usar `Invoke-RestMethod` do PowerShell.

```powershell
$token = "Bearer SEU_TOKEN"
$folderId = "ID_DO_FOLDER_NO_ORCHESTRATOR"
$nupkgPath = "C:\...\LibraryName.1.550.8.nupkg"

Invoke-RestMethod `
  -Uri "https://cloud.uipath.com/{org}/{tenant}/orchestrator_/odata/Processes/UiPath.Server.Configuration.OData.UploadPackage" `
  -Method Post `
  -Headers @{
    "Authorization" = $token
    "X-UIPATH-OrganizationUnitId" = $folderId
  } `
  -Form @{ file = Get-Item $nupkgPath }
```

### Verificar publicação

1. Acessar Orchestrator → Packages
2. Filtrar pelo nome da library
3. Confirmar que a nova versão aparece na lista

### Atualizar processos dependentes

Após publicar a library, atualizar a dependência nos processos que devem usar a nova versão. Ver Runbook 6.

---

*Fim dos runbooks — versão 1.0 — 2026-06-03*
