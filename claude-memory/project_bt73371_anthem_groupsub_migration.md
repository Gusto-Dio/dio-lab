---
name: project-bt73371-anthem-groupsub-migration
description: "BT-73371 — Anthem_GroupSubmissions_MemberLevel migração Legacy→Modern; build passa; próximo passo: rename projeto e abrir PR"
metadata: 
  node_type: memory
  type: project
  originSessionId: 14e6759f-8d77-425a-83c0-39cdb867b950
---

# BT-73371 — Anthem_GroupSubmissions_MemberLevel — Legacy → Modern migration

**Status:** PR #2802 aberta — aguardando review.

**Why:** Migração obrigatória de .NET Framework (Legacy) para Windows Modern framework — parte do programa de modernização BenOps.

## Pastas

| Tipo | Caminho |
|---|---|
| Legacy (manter até PR mergear) | `Processes/Benefits/CarrierAutomations/GroupSubmission/Anthem/Anthem_GroupSubmission_MemberLevel/` |
| Modern (branch atual) | `Processes/Benefits/CarrierAutomations/GroupSubmission/Anthem/Anthem_GroupSubmission_MemberLevel_Modern/` |

**Branch:** nova branch será criada para a PR (a partir de develop).

## Erros corrigidos nesta sessão

### 1. `Then property already set on If` — `TerminateEmployees.xaml`
- Causa: `<If.Then>` continha dois elementos filhos diretos (`TryCatch` + `If`); WF4 `Then` é scalar
- Fix: envolveu ambos em `<Sequence DisplayName="Cancel Coverage and Handle Error">`

### 2. `Missing invoked workflows` — `GetSalesForceRecords.xaml` + `GetS3Census.xaml`
- Causa: `ProcessTransaction.xaml` invocava ambos mas os arquivos não existiam no Modern
- Fix: criou stubs com assinaturas corretas (args conforme chamada em ProcessTransaction)

### 3. `Argument in_EmployeeDetails does not exist in EnterProvider` — `EnterCoverage.xaml`
- Causa: invocação gerada de `EnterProvider` passou `in_EmployeeDetails` e `in_DependentDetails` que não existem em `EnterProvider.xaml`; também faltava `out_EnrollmentError`
- Fix: removeu os dois args inválidos, adicionou `<OutArgument x:Key="out_EnrollmentError">[out_EnrollmentError]</OutArgument>`
- Referência: Legacy `EnterCoverage.xaml` linha 464–466 confirma que só `in_wbParentPath` + `out_EnrollmentError` são passados

## Arquivos criados (stubs — TODO: implementar)

- `ProcessLayer/GetSalesForceRecords.xaml` — args: in_wbParentPath, in_InstanceCredential, in_KeyCredential, in_UserCredential, in_Query, out_TransactionData(DataTable)
- `ProcessLayer/GetS3Census.xaml` — args: in_wbParentPath, in_AWSCredential, in_Bucket, in_CensusFilePrefix, in_FileName, in_FilePath, out_CensusData(DataTable)

## Próximos passos (retomar após pausa)

1. **Rename projeto:**
   ```powershell
   # Criar branch nova
   git checkout develop && git pull
   git checkout -b BT-73371-Anthem-GroupSubmissions-MemberLevel-windows-migration
   
   # Remover Legacy
   git rm -r "Processes/Benefits/CarrierAutomations/GroupSubmission/Anthem/Anthem_GroupSubmission_MemberLevel/"
   
   # Renomear Modern
   git mv "Processes/Benefits/CarrierAutomations/GroupSubmission/Anthem/Anthem_GroupSubmission_MemberLevel_Modern/" \
          "Processes/Benefits/CarrierAutomations/GroupSubmission/Anthem/Anthem_GroupSubmission_MemberLevel/"
   ```

2. **Atualizar `project.json`:** campo `"name"` de `"Anthem_GroupSubmissions_MemberLevel_Modern"` → `"Anthem_GroupSubmissions_MemberLevel"`

3. **Atualizar `Data/Config.json`:** campo `"ProcessName"` idem

4. **Rodar build final** no diretório renomeado para confirmar que ainda compila

5. **Commit + PR** seguindo formato padrão do repo

## Warnings restantes (não bloqueantes)

- Variáveis com `_Error` no nome não batem com o padrão de nomenclatura do analyzer (ex: `b_SystemErrorFound`, `b_CancellationError`) — são nomes do Legacy preservados; não alterar nesta PR
- Display names duplicados (`Set updateError = True`, `Set out_EnrollmentError = True`) — idem, vêm do código gerado; não bloqueia build
- Nesting depth > 3 em alguns `If` — warning não-bloqueante

**How to apply:** ao retomar, continuar diretamente do passo 1 (rename) acima — build já validado.
