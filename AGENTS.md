# Guía para Agentes

Normas y convenciones para agentes de desarrollo en este repositorio.

## 1. Commits y PR

Conventional Commits v1.0.0 (spec estricta, sin desviaciones). Formato:

```text
<tipo>(<alcance>)?(!)?: <sujeto>
<línea en blanco>
<cuerpo>
<línea en blanco>
<footer>
```

PR debe indicar qué cambia y por qué, no solo qué archivos.

### 1.1 Reglas de la spec (MUST, no negociables)

Directo de conventionalcommits.org v1.0.0 — violar cualquiera de estas invalida
el commit como Conventional Commit, no es cuestión de estilo:

- Header: `tipo` + alcance opcional entre paréntesis + `!` opcional + `:` +
  espacio único + sujeto. Sin espacio antes de dos puntos, sujeto arranca
  justo tras dos puntos y espacio.
- `feat` únicamente para funcionalidad nueva (MINOR en semver). `fix` únicamente
  para corrección de bug (PATCH en semver).
- Cuerpo, si existe, separado del header por exactamente una línea en blanco.
- Footer, si existe, separado del cuerpo por una línea en blanco. Formato git
  trailer: `Token: valor` o `Token #valor`. El token usa guiones en vez de
  espacios (`Reviewed-by`, `Refs`, no "Reviewed by"). El valor de un footer
  puede extenderse en varias líneas hasta que aparece el siguiente token válido.
- Breaking change — dos formas, no excluyentes, con una alcanza:
  1. Footer `BREAKING CHANGE: <descripción>` (token en mayúsculas —
     única unidad case-sensitive; `BREAKING-CHANGE` es sinónimo válido).
  2. `!` inmediatamente antes de los dos puntos del header: `feat(scope)!: ...`.
  Un breaking change en cualquier tipo (no solo `feat`/`fix`) fuerza MAJOR en
  semver.
- `revert`: sujeto describe el commit revertido; footer obligatorio `This
  reverts commit <hash-completo>.`
- Tipos fuera de `feat`/`fix`/breaking (`docs`, `style`, `refactor`, `perf`,
  `test`, `build`, `ci`, `chore`, `revert`) son permitidos por la spec pero no
  aportan bump de semver por sí solos.

### 1.2 Gitmoji (opcional)

Formato con Gitmoji: `:emoji: <tipo>(<alcance>)?(!)?: <sujeto>`.

- Emoji obligatorio al inicio de todo commit, prioridad de menor a mayor:
  1. Gitmoji por defecto según tipo (gitmoji.dev), con el significado oficial de
     cada uno — el mapeo coincide con la semántica del catálogo:
     - `feat` → ✨ (*introduce new features*)
     - `fix` → 🐛 (*fix a bug*)
     - `docs` → 📝 (*add or update documentation*)
     - `style` → 🎨 (*improve structure/format of the code*)
     - `refactor` → ♻️ (*refactor code*)
     - `perf` → ⚡️ (*improve performance*)
     - `test` → ✅ (*add, update or pass tests*)
     - `build` → 📦️ (*update compiled files or packages*)
     - `ci` → 👷 (*add or update CI build system*)
     - `chore` → 🔧 (*config/tooling change*)
     - `revert` → ⏪️ (*revert changes*)
  2. Gitmoji específico del catálogo si encaja mejor: 💥 breaking, 🎉 inicio
     proyecto, 🔥 quitar código, 💄 UI, 🔒 seguridad, 🚀 deploy.
  3. Emoji personalizado para dominio del proyecto (ej. 🐋 al tocar Docker) —
     libre si el significado no es ambiguo.
- Excepción: merge commits y bots (dependabot) no se reescriben a este formato.
- No contradice la regla de firma de agente arriba: el emoji es semántico (tipo
  de cambio), no atribución de autoría — sigue sin ir `Co-Authored-By` ni
  equivalentes salvo pedido explícito.
