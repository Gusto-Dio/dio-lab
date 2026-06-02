---
name: anthem-stability-page-transition
description: Melhoria de estabilidade pendente no Anthem_NewHireEnrollment — adicionar waits de carregamento entre transições de página
metadata: 
  node_type: memory
  type: project
  originSessionId: 14958709-7532-4eed-a55f-f73ec95f83a9
---

# Anthem NewHireEnrollment — Estabilidade entre páginas

**Pendência:** Adicionar waits de carregamento de página mais robustos em `EnterDependentsInformation.xaml` (e possivelmente outros XAMLs do processo).

**Problema observado (2026-05-13):** Durante teste de transação, um `UiElementExists` retornou `False` porque a página ainda estava carregando no momento da verificação. O seletor era válido mas a página não tinha terminado de renderizar.

**Why:** Seletores corrigidos e transações passando, mas há risco de flapping entre transações em condições de rede mais lentas.

**How to apply:** Ao retomar, revisar cada Invoke que transita de página no processo Anthem (NavigateToEnrollment, EnterEmployeeInformation, EnterDependentsInformation, etc.) e adicionar `WaitForReady` adequado ou um `UiElementExists` com retry antes de continuar.

**Status:** PENDENTE — retomar após merge das PRs abertas (#2624, #2625, #2570).
