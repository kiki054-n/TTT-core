# TTT Proof Status

## Tri-Tetra Theory — Proof, Evidence, Unproven Parts, and Refutation Conditions

**Project:** Tri-Tetra Theory (TTT)
**Document:** `PROOF_STATUS.md`
**Version:** 2.1
**Status:** Research-stage formalization
**Date:** 2026-09-06
**Supersedes:** v1.0 (2026-09-05), v2.0 (2026-09-06)

---

## 0. Purpose

This document records the current proof status of the principal statements in the TTT Definition Ledger.

The purpose is **not** to declare that TTT has been scientifically established.

Each statement is separated into:

1. **Definition** — What is being defined?
2. **Premises** — What assumptions or known results are being used?
3. **Derivation** — What follows rigorously from those premises?
4. **Conclusion** — What can legitimately be claimed, and at what level?
5. **Unproven parts** — Which additional TTT claims have not yet been established?
6. **Refutation conditions** — What observation, calculation, or logical contradiction would invalidate the claim?

Two rules govern the whole document:

> A mathematical proof of an internal relation is not a proof of a physical interpretation.

> A numerical agreement with experiment is not a derivation from TTT axioms.

---

## 0.1 Changes from v1.0

v1.0 was internally consistent in its arithmetic — every calculation in it has been independently re-verified and none is wrong. The revisions below concern **structure**, not computation.

| # | Change | Reason |
|---|---|---|
| 1 | Status scale replaced: `M3/M2/M1/E/U/R` → `A/D/B/E/C/O/F` | v1.0 defined M3 as "a direct logical consequence of explicitly stated premises," which promotes every tautology to theorem level. Under it, $\pi=-1$ (one line of algebra from two TTT stipulations) and the crystallographic restriction theorem received the same grade. The new level **D (definition)** separates them. |
| 2 | **A now requires attribution** | Of the statements that reach theorem level, all are borrowed from external mathematics. TTT has not yet proven a theorem of its own. This must be visible in the table, not buried in prose. |
| 3 | **R2 downgraded from refuted to open** (→ O1) | v1.0 rejected $648=501+147$ "within the stated TTT counting rules," while U3 simultaneously declared those counting rules undetermined. A rejection resting on an unresolved premise is not a rejection. |
| 4 | R3's contested part relocated to O1 | $147 \neq 37\times4$ is unconditionally false and stays refuted. The live question — whether the overflow quantity is 147 or 148 — is decided by the energy scale, not by arithmetic. |
| 5 | U1, U4, U5, U6 merged into **O1** | All four are the same single problem: there is no rule assigning physical units to TTT quantities. Listing four made the remaining work look larger and less focused than it is. |
| 6 | U2 upgraded U → **B**, with a derivation | $\partial\partial=0$ settles the shared-boundary question. It was recorded in the ledger but left as unresolved here. |
| 7 | New §7 (Lie-operator audit), §8 (mass-ratio audit), §9 (post-correction retest) | v1.0 was dated 2026-09-05 and predates these three audits, including the null-control result that is the sharpest instrument in the project. |
| 8 | **Null control added to the required proof chain** (§11) | v1.0 stated the principle that numerical agreement is not derivation (§27) but supplied no procedure for enforcing it. |
| 9 | **Unit-conversion rule added as an explicit chain step** (§11) | The audits identify O1 as the single largest gap; a chain that does not name the step cannot expose the gap. |
| 10 | Refutation conditions rewritten to be external | Several v1.0 conditions were circular ("fails if it cannot be derived"). A refutation condition must live outside the theory. |
| 11 | LaTeX delimiters `\[ \]` → `$$ $$` | `\[ \]` does not render on GitHub or Zenodo. |
| 12 | Numerical targets stated at their measured precision | e.g. $m_p/m_e = 1836.15267343(11)$, not 1836. |

## 0.2 Corrections in v2.1

Two errors in v2.0, found by checking it against the Definition Ledger. Both are recorded rather than silently repaired, per §27.

**(a) R2 and R3 were attached to the wrong open problem.** v2.0 sent both to O3 (structural count). They belong to **O1** (unit-conversion rule).

The reason is arithmetic v2.0 failed to carry out:

$$125.25\times4 = 501, \qquad 648-501 = 147.$$

Read as a **count**, TTT gives $125\times4=500$ and the split is $500+148$. Read as an **energy** at O$\pi$O granularity, 125.25 gives exactly 501 and the split is $501+147$. Both are internally coherent; which one applies is decided by the energy scale (O1), not by the count (O3). That $147/4=36.75$ is not an obstacle under the energy reading, since energies need not be multiples of four — but the price of that reading is that "37 tetrahedra" must be abandoned, because 37 is a *count* claim about an *energy* quantity, which the type rule forbids.

Forbidden under either reading: writing $500+148$ and $501+147$ **as the same split** in one document.

**(b) P2 and P7 were graded too harshly.** v2.0 marked both D. The instances are definitions, but each rests on a borrowed theorem that does real work, and the table should show it:

- **P2** — identifying $X,Y,Z$ with half-turns is D; Hamilton's $ijk=-1$ and $U(2\pi)=-\mathbb{1}$ in $SU(2)$ are A. The A stands on top of the D.
- **P7** — the instance $5+2=7$ is D, but the general statement $V(n)=n+2$ for a bipyramid follows from Euler's formula ($V-E+F=2$ with $E=3n$, $F=2n$), which is A.

The headline conclusion is unchanged: every theorem-level result in this file is borrowed, and TTT has proven none of its own.

---

# 1. Proof-status levels

| Level | Meaning |
|---|---|
| **A** | **Theorem.** Mathematically proven. **Attribution is mandatory** — the entry must name whose theorem it is. |
| **D** | **Definition.** True by stipulation, or a one-step restatement of stipulations. Valid, but carries no information beyond the definitions. |
| **B** | **Proposition.** Follows validly from TTT-internal premises that are not themselves independently justified. |
| **E** | **Empirical.** Supported by measurement or observation. Not a mathematical proof. |
| **C** | **Hypothesis.** Mathematically coherent, derivation incomplete. |
| **O** | **Open.** The problem is stated but not solved; no derivation exists yet in either direction. |
| **F** | **Refuted** under the present definitions and assumptions. |

### Rules of use

> **A does not mean "physically true."**
> It means the mathematical statement is proven. The bridge to physical reality is a separate obligation.

> **D is not a weaker A.**
> A statement that follows in one step from stipulations that were chosen to produce it is a definition, however valid the algebra. Grading it A inflates the theory's mathematical content.

> **A borrowed theorem is still A, but it is not a TTT result.**
> Using the crystallographic restriction theorem correctly is good practice. It is not evidence that TTT proves things.

> **A compound label (e.g. `A + C`) means the mathematical core is proven and the TTT claim built on it is not.** The two must never be reported as one grade.

---

# 2. Summary table

## 2.1 Structural statements (P)

| ID | Subject | Math core | TTT claim | Attribution of the math core |
|---|---|:---:|:---:|---|
| **P1** | Bipolar zero / curvature | **D** | **C** | $\kappa=1/r$ is the definition of curvature |
| **P2** | $\pi=-1$ / spin | **D + A\*** | **C** | Hamilton ($ijk=-1$); $SU(2)$ double cover |
| **P3** | Boundary as threshold | **A + E** | **C** | Elementary analysis; hydrogen ionization |
| **P4** | Birth and emission | **A + E** | **C** | Conservation laws; radiative capture |
| **P5** | Mass sign and escape | **A + E** | **C** | Mass–energy equivalence; QCD confinement |
| **P6** | Fivefold restriction / generations | **A** | **C** | Crystallographic restriction theorem |
| **P7** | Pentagonal bipyramid = 7 | **D + A\*** | **C** | Euler's formula: $V(n)=n+2$ |
| **P8** | Centre quantity / boundary | **A + E** | **C** | Hydrostatic equilibrium |

**\*** — the theorem is borrowed and stands on top of a TTT definition: it is used correctly, but it is not evidence that TTT proves things. See §0.2(b).

**Reading of this table.** Exactly one entry (P6) reaches theorem level *for the statement TTT actually wants to make*, and that theorem is borrowed. P3, P4, P5 and P8 correctly use established physics as premises, but the TTT generalisation built on each is at hypothesis level. P1 is a definition; P2 and P7 are definitions carrying a borrowed theorem.

> **TTT has not yet proven a theorem of its own.**
>
> This is a weakness, but not a bad state to be in. Borrowed theorems are hard, and using them knowingly does not lead to error. The failure mode is mistaking a borrowing for a discovery.

## 2.2 Refuted statements (F)

| ID | Subject | Level | Core result |
|---|---|:---:|---|
| **R1** | $1836=3\times648$ | **F** | $3\times648=1944$. Also, the target is $1836.152673$, not an integer |
| **R3** | $147=37\times4$ | **F** | $37\times4=148$. (Whether the overflow is 147 or 148 → **O1**) |
| **R4** | $37=1+30$ | **F** | $1+30=31$ |
| **R5** | Supercritical fluid as a fusion route | **F (E)** | Energy-scale mismatch of ~6 orders of magnitude |
| **R6** | Fleming's law → $XYZ$ | **F (A)** | Vector / pseudovector transformation mismatch |
| **R7** | Five fingers as structural basis | **F (E)** | Biological contingency; $D_{5h}$ is achiral |
| ~~R2~~ | $648=501+147$ | *moved* | Was F in v1.0; its rejection depended on the unresolved energy scale → **O1** |

## 2.3 Open problems (O)

| ID | Subject | Level | Absorbs | Core issue |
|---|---|:---:|---|---|
| **O1** | Unit-conversion rule | **O** | U1, U4, U5, U6, R2, part of R3 | No rule maps TTT quantities to physical units |
| **O2** | Boundary component count | **B** | U2 | $\partial\partial=0$ gives 4, not 5; needs formalising |
| **O3** | Structural count 124 / 125 / 128 | **O** | U3, part of R4 | Which count is fundamental is undetermined |
| **O4** | Fermionic representation | **O** | U7 | No construction yields $U(2\pi)\psi=-\psi$ |

Seven listed unknowns reduce to four, of which one (O2) already has a derivation.

## 2.4 Audit findings (2026-09-06)

| ID | Subject | Level | Core result |
|---|---|:---:|---|
| **M1–M2** | Transition operators $T_i$, spectrum | **A** | Minimum-Frobenius-norm solution correct; all figures reproduced |
| **M3–M11** | Triple root, 9-dimensional closure, rank-1 dominance, invariant ratio, conservation law, golden-ratio proofs | **F** | Constructive artifacts, unit-dependent quantities, and three unrepaired errors |
| **M12–M13** | Fibonacci convergence, fractal dimension | **C** | Incomplete proof (repairable); no basis given |
| **G1** | 17-mass reproduction | **F** | 7 of 17 masses off by 55–99%; the quoted ratio column contains measured, not predicted, values |
| **G2–G3** | W/Z/H and tau implementations | **F → repaired** | Implementation errors, not theory errors. Corrected in §9 |
| **G4–G5** | "No free parameters" | **F** | At least 9 hand-placed constants for 17 masses |
| **G6** | Attribution of sections A, C, D, E, F, G | **O** | Correct summaries of existing literature; sources must be cited |
| **G7** | $k\pi R\approx39.14$ | *minor* | $e^{-k\pi R}=1.0\times10^{-17}$, table says $2\times10^{-17}$ |
| **N1** | Null control on mass ratios | **F** | 71.9% of random targets reachable within 1% using the same vocabulary |

---

# 3. P1 — Bipolar zero and curvature

## Definition

TTT introduces the bipolar relation

$$Y=\frac{1}{X}$$

and interprets it geometrically through curvature and radius:

$$\kappa=\frac{1}{r}.$$

The limiting cases are

$$r\rightarrow\infty \Rightarrow \kappa\rightarrow0, \qquad r\rightarrow0^{+} \Rightarrow \kappa\rightarrow\infty.$$

TTT calls the corresponding zero-limit structure a *bipolar zero*.

## Premises

1. Curvature of a circle is **defined** as $\kappa = 1/r$.
2. Reciprocal quantities generate a bipolar relationship.
3. The limiting behaviour of $1/r$ is well defined in the extended sense.

## Derivation

From $\kappa=1/r$,

$$\lim_{r\rightarrow\infty}\kappa=0, \qquad \lim_{r\rightarrow0^{+}}\kappa=\infty.$$

Radius and curvature are reciprocal descriptions of the same object.

## Conclusion

**Math core: D. TTT claim: C.**

The reciprocal relation is not a theorem — it is what "curvature" means. Nothing is derived here; the content lies entirely in the proposal to treat this reciprocity as fundamental, which is a hypothesis.

The one genuinely useful consequence is interpretive and worth stating plainly: the bipolar zero axiom ("nothing can exist at the zero point") becomes "infinite curvature cannot exist," which is a statement with geometric meaning rather than a slogan.

## Unproven parts

1. That $Y=1/X$ is a fundamental physical axiom.
2. That physical existence is governed by this reciprocal structure.
3. That $r=0,\ \kappa=\infty$ is physically impossible rather than merely singular.
4. That this principle generates the remaining TTT structures.

## Refutation conditions

**External form.** P1 is not refutable as stated, because a definition cannot be refuted — this is itself the finding. To become testable, the axiom must forbid something. Candidate: if TTT asserts that no physical configuration reaches $\kappa=\infty$, then a confirmed physical singularity of finite extent (as opposed to one hidden behind a horizon or removed by quantum gravity) refutes it. Until the axiom is stated in a form that forbids an observable, P1 contributes no testable content.

---

# 4. P2 — $\pi=-1$, double rotation, and spin

## Definition

TTT introduces a quantity written $\pi$ with value

$$\pi=-1.$$

This is **not** the circle constant $3.14159\ldots$. The definition rests on

$$XYZ=-1, \qquad XYZ\pi=1.$$

## Premises

1. $XYZ=-1$ — a TTT stipulation.
2. $XYZ\pi=1$ — a TTT stipulation.
3. TTT uses $\pi$ as a rotation/state operator, not as the numerical constant.
4. In spinor mathematics a $2\pi$ rotation produces a sign change.

## Derivation

From $XYZ\pi=1$ and $XYZ=-1$,

$$(-1)\pi=1 \quad\Longrightarrow\quad \pi=-1.$$

## Conclusion

**Math core: D + A (borrowed). TTT claim: C.**

v1.0 graded this M3. The algebra is valid, but both premises are TTT stipulations chosen so that this result follows. One line of arithmetic from two chosen premises is a definition restated, not a theorem — hence **D**.

What *is* at level A is external and must be attributed: Hamilton's $ijk=-1$, and $U(2\pi)=-\mathbb{1}$ in $SU(2)$. If $X,Y,Z$ are read as half-turns about three axes, TTT's $\pi$ is structurally the same object as the non-trivial element of the double cover, and the sign is then a theorem rather than a stipulation.

**The A stands on top of the D.** The reading of $X,Y,Z$ as half-turns is the definition; everything hard that follows is Hamilton's. Grading the entry A alone would credit TTT with the double cover; grading it D alone would discard a genuine and useful identification. Both parts must be shown.

## Unproven parts

1. That TTT's $\pi$ is the $2\pi$-rotation operation rather than merely obeying the same sign rule.
2. That the construction necessarily generates fermions (→ **O4**).
3. That it explains the Standard Model spin structure.
4. That the spin label $\sigma$ follows uniquely.

## Refutation conditions

**External form.** TTT must construct a representation in which a state $\psi$ built from its own structure satisfies $U(2\pi)\psi=-\psi$, with the sign emerging rather than inserted. If every representation constructible from TTT's stated objects is integer-spin, the spin interpretation is refuted. This is the same obligation as O4 and should be discharged once.

**Notational hazard.** TTT's rotational $\pi$ and the pion $\pi$ (mediator of the nuclear force, 139.57 MeV) are unrelated objects that share a character by accident. Any document that mixes them in one argument is unsound regardless of its content.

---

# 5. P3 — Boundary as threshold

## Definition

TTT defines a boundary not as a hard spatial surface but as a threshold separating states.

For a bound state, $\psi(r)\sim e^{-r/a_0}$ does not reach zero at any finite $r$. TTT therefore identifies the physically relevant boundary with an energy threshold such as the ionisation energy.

## Premises

1. Bound-state wavefunctions have non-vanishing tails.
2. A bound-to-free transition is characterised by an energy threshold.
3. The hydrogen ionisation threshold is $13.598434$ eV.

## Derivation

$e^{-r/a_0}$ approaches zero only asymptotically, so no finite radius exists at which the wavefunction must vanish. The bound/free distinction is therefore an energy condition, not a geometric one.

## Conclusion

**Math core: A + E. TTT claim: C.**

The mathematics is elementary and correct; the empirical anchor is solid. The general claim — that *every* physical boundary is a threshold — is a hypothesis.

This reframing is the most productive move in the P-series, because it converts "boundary" from a picture into a quantity that can be measured.

## Unproven parts

1. That every physical boundary is representable as a threshold.
2. That the same boundary principle governs particles, atoms and the universe.
3. That massless particles correspond to systems without a relevant threshold.

## Refutation conditions

**External form.** Exhibit a physical boundary that (a) is operationally sharp, (b) is not associated with any state transition, and (c) cannot be recast as a threshold in any variable. A domain wall in a ferromagnet or a first-order phase boundary would be the natural place to look; if the threshold reading survives those, the hypothesis has earned something.

---

# 6. P4 — Birth and emission

## Definition

TTT proposes that a new bound structure is created through a transition in which energy and momentum must be redistributed, generally involving emission. Example:

$$n+p\rightarrow d+\gamma,$$

releasing $2.224566$ MeV.

## Premises

1. Energy conservation.
2. Momentum conservation.
3. Initial and final systems have different binding energies.
4. A two-body initial state cannot in general become a single bound object while conserving both energy and momentum without an additional degree of freedom.

## Derivation

In radiative capture the photon removes energy and momentum; the released binding energy appears as radiation and recoil.

## Conclusion

**Math core: A + E. TTT claim: C.**

The conservation argument is rigorous for this reaction class and is standard physics. The universal statement "birth always involves emission" needs qualification: the emitted object need not be a photon, and in three-body and medium-assisted processes the third degree of freedom can be another nucleus, an electron, or the surrounding lattice.

This statement carries real weight inside TTT, because it supplies the sign rule that P5 needs: what escapes lowers the mass; what cannot escape raises it.

## Unproven parts

1. That every form of physical birth emits a photon specifically.
2. That every TTT state transition requires an emitted particle.
3. That the emission principle alone determines particle masses.

## Refutation conditions

**External form.** A reproducible state-formation process satisfying all conservation laws with no third degree of freedom refutes the universal form. Internal conversion and three-body capture are the standard cases to check the statement against before publishing it.

---

# 7. P5 — Mass sign and escape criterion

## Definition

TTT proposes that the sign and magnitude of a mass contribution follow from whether energy can escape a structure.

Binding-energy release lowers the mass of a bound system, e.g. $m_d < m_p+m_n$. TTT contrasts this with the proton, whose constituent quark masses account for roughly 1% of the observed mass, the remainder being QCD field and kinetic energy that cannot escape.

## Premises

1. Mass–energy equivalence.
2. Binding energy contributes negatively to the mass of a bound system.
3. Colour confinement prevents free separation of quarks.
4. Field energy contributes to the total invariant mass.

## Derivation

$$M_{\rm bound}c^{2}=\sum_i m_i c^{2}-E_{\rm binding}.$$

For a confined system the total energy includes field and kinetic contributions that no emission can remove.

## Conclusion

**Math core: A + E. TTT claim: C.**

Each ingredient is established physics. The TTT generalisation — that *escape capability* determines the sign — is a model-level interpretation, but a good one: it resolves a genuine internal contradiction (why "boundary formation = mass" holds for the proton and reverses for nuclei and atoms) using a single criterion.

## Unproven parts

1. A universal mathematical definition of "escape."
2. A derivation of any particle mass from this criterion.
3. A unique TTT mass equation.

## Refutation conditions

**External form.** Identify a class of systems in which the sign of the mass defect is opposite to what the escape criterion predicts. The criterion must be stated sharply enough first — "escape" needs a definition in terms of asymptotic states, not intuition.

---

# 8. P6 — Fivefold restriction and generations

## Definition

TTT connects the number of generations to the crystallographic restriction theorem. A rotational symmetry compatible with a periodic lattice requires

$$1+2\cos\!\left(\frac{2\pi}{n}\right)\in\mathbb{Z},$$

allowing only

$$n=1,2,3,4,6.$$

Fivefold periodic rotational symmetry is excluded from ordinary translational lattices, since $2\cos 72^\circ = 1/\varphi = 0.6180\ldots$ is irrational.

## Premises

1. The crystallographic restriction theorem.
2. The allowed orders are $1,2,3,4,6$.
3. Fivefold symmetry is incompatible with ordinary periodic lattices.
4. TTT maps a structural hierarchy onto particle generations.

## Derivation

The crystallographic restriction is a proven theorem. However,

$$\text{crystallographic restriction} \;\nRightarrow\; \text{maximum of five physical generations}.$$

The implication requires a TTT-specific mapping that has not been supplied.

## Conclusion

**Math core: A (crystallographic restriction theorem, external). TTT claim: C.**

**This is the strongest entry in the P-series.** It is the only place where a real theorem does real work in the argument: it explains why a fivefold structure cannot be accommodated in a translational lattice, which is exactly the "overflow" TTT needs.

**Necessary caveat.** The theorem forbids fivefold symmetry *in periodic lattices*, not fivefold symmetry as such. Quasicrystals (Shechtman 1982; Nobel Prize in Chemistry 2011; Al–Mn, Al–Pd–Mn, and the natural mineral icosahedrite) realise fivefold order aperiodically. If TTT wants the overflow to be a real degree of freedom rather than a prohibition, the existing physical concept is the **phason**, and that is where the mapping should attach.

## Unproven parts

1. Why generations should correspond to crystallographic rotational order at all.
2. Why $n=5$ specifically represents a generation limit.
3. Why observed generations should terminate at five rather than at three.
4. Whether the proposed cubic/icosahedral duality is physically realised.

## Refutation conditions

**External form.** State the map $n \mapsto$ generation explicitly, then check that it forbids a fourth generation *on structural grounds*. This is an unusually good test, because the fourth generation is already excluded experimentally — the invisible $Z$ width gives $N_\nu = 2.9840 \pm 0.0082$ for light neutrino species. If the TTT map permits four, it is refuted by an existing measurement. If it forbids four but its only reason is that the answer is known, it has explained nothing. The map must be written down before the count is compared.

---

# 9. P7 — Pentagonal bipyramid and 7

## Definition

TTT identifies the number seven with the vertices of a pentagonal bipyramid:

$$5+2=7,$$

five equatorial vertices (pentagonal structure) plus two axial vertices (bipolar structure).

## Premises

1. A pentagonal bipyramid has five equatorial and two axial vertices.
2. TTT restricts the relevant structural order to the range implied by P6.

## Derivation

Direct counting gives $5+2=7$.

## Conclusion

**Math core: D + A (borrowed). TTT claim: C.**

The instance $5+2=7$ is a count — **D**. v1.0 graded it M3 and called it "mathematically exact"; it is exact, and it is arithmetic. Grading arithmetic as a proven theorem inflates the theory's mathematical content, which is the failure mode this document exists to prevent.

The general statement is stronger and is **A**: for a bipyramid on an $n$-gon, $E=3n$ and $F=2n$, so Euler's formula $V-E+F=2$ gives

$$V(n)=n+2.$$

That is a theorem — Euler's — and it does real work, because it shows the vertex count is forced rather than chosen.

But note what it forces. $V(n)=n+2$ is satisfied by *every* $n$, so on its own it generates every integer above 2 and privileges nothing. The content lies entirely in the restriction $n\le5$, which is P6's crystallographic argument. Combined, the vertex count closes on $\{5,6,7\}$ — three values, not one. **Seven is the largest member of a small set, not a singled-out number.** The credit belongs to P6, and the honest statement of P7 is that 7 is *available* in the vocabulary, not that it is *derived*.

## Unproven parts

1. That seven is physically privileged.
2. That the pentagonal bipyramid is the correct structural representation.
3. That the structure explains observed appearances of seven.

## Refutation conditions

**External form.** Name one physical seven that the structure predicts *before* it is looked up, together with the reason no other integer could appear there. Absent that, P7 is a naming convention.

**Note.** $D_{5h}$ possesses mirror planes and is therefore achiral. Any argument that draws handedness from the sevenfold *shape* is unsound; chirality can enter only as a cyclic ordering (a sign), never as the geometry itself.

---

# 10. P8 — Centre quantity and boundary determination

## Definition

TTT proposes that a centre quantity is not determined by its local value. Earth is the example: $g=0$ at the exact centre while pressure is maximal.

## Premises

1. Hydrostatic equilibrium, $\dfrac{dP}{dr}=-\rho g$.
2. Gravitational acceleration vanishes at the centre of a spherically symmetric body.
3. Pressure depends on the integrated mass distribution above the point.

## Derivation

At the centre $g(0)=0$, but

$$P(r)=P(R)+\int_r^R \rho(r')\,g(r')\,dr'.$$

Hence $g=0$ locally does not imply $P=0$.

## Conclusion

**Math core: A + E. TTT claim: C.**

The hydrostatic example is correct and well chosen. The generalisation to "centre quantities" as a class is a hypothesis.

The underlying observation — that a local differential quantity can vanish while its integral does not — is true and general, but it is a property of integration, not of centres. Stating it that way makes the claim honest and simultaneously reveals how little it constrains.

## Unproven parts

1. That this is a universal property of "centre quantities."
2. That the principle generates TTT's centre state.
3. That it explains the centre quantity in particle/universe duality.

## Refutation conditions

**External form.** The generalisation must forbid something. If TTT claims a centre quantity is always determined by the boundary, that is a statement of the same type as the holographic principle and should be tested where that principle is tested, not asserted by analogy.

---

# 11. R1 — $1836=3\times648$

## Statement

$$\frac{m_p}{m_e}=1836, \qquad 1836=3\times648.$$

## Refutation

$$3\times648=1944 \neq 1836.$$

Additionally:

$$1836=2^{2}\times3^{3}\times17,$$

and the factor 17 lies outside the stated $\{2,3,5\}$ vocabulary.

**Second, independent problem.** The target is not 1836. The measured ratio is

$$\frac{m_p}{m_e}=1836.15267343(11).$$

Aiming at the integer already discards a known quantity at the $10^{-4}$ level. A structural theory that predicts an integer must say why the physical value is not one.

The observation that $648:1836 = 6:17$ is arithmetically correct and evidentially worthless on its own.

## Conclusion

**F.** The decomposition is arithmetically false, and the target was misstated.

## Refutation conditions

Overturnable only by changing the original statement — i.e. by replacing 648 or 3 with different quantities, which would be a new claim requiring its own derivation and its own null control (§17).

---

# 12. R3 — $147=37\times4$

## Statement

$$147=37\times4.$$

## Refutation

$$37\times4=148 \neq 147.$$

## Conclusion

**F.** Unconditionally false.

## What remains open

The arithmetic is settled. The live question is a different one: **is the overflow quantity 147 or 148?** That is decided by whether the quantity is read as a count or as an energy, i.e. by the unit-conversion rule. It is tracked under **O1**, not here.

Note that $147/4 = 36.75$ disqualifies 147 only under the *count* reading. Energies need not be multiples of four, so an energy reading admits 147 — at the cost of abandoning "37 tetrahedra," since 37 is a count claim about an energy quantity, which the type rule forbids. **The choice is between keeping 147 as an energy and keeping 37 as a count. Not both.**

This separation matters. The contested content of R3 is not its arithmetic but which quantity the arithmetic applies to. Marking the false identity F while relocating the real question to O1 preserves both the rejection and the dispute.

---

# 13. R4 — $37=1+30$

## Statement

$$37=1+30.$$

## Refutation

$$1+30=31 \neq 37.$$

30 is correctly the edge count of the icosahedron and dodecahedron, but that number does not connect to 37 by this decomposition.

## Conclusion

**F.**

## Refutation conditions

None under ordinary arithmetic. A different decomposition of 37 may exist; it cannot use this equality.

**Related unresolved issue.** 37 is odd, while the bipolar-zero axiom requires objects to appear in pairs. A strict parity argument over a $5\times5\times5$ cell gives $125=2\times62+1$: 62 pairs fit and one cell necessarily remains unpaired, so the overflow is 38, not 37. This was noted on 2026-08-08 (the $37\to74$ revision) and remains unsettled. It is folded into **O3**, since it is a question about counts.

A separate route to overturning R4, recorded in the ledger: obtain the difference 6 from within the vocabulary (the octahedron has six vertices). That would be a new claim requiring its own derivation and its own null control.

---

# 14. R5 — Supercritical water / CO₂ as a fusion route

## Statement

Supercritical water or CO₂ conditions promote nuclear fusion.

## Premises

1. Nuclear forces act at femtometre scales.
2. Chemical interactions occur at atomic scales.
3. Chemical thermal energies are far below nuclear energies.
4. Supercritical conditions do not create nuclear-scale confinement.

## Refutation

Nuclear scale: keV–MeV. Chemical thermal scale near the critical point of water ($T_c = 647$ K):

$$kT = 8.617\times10^{-5}\,\text{eV/K}\times647\,\text{K}=0.0558\ \text{eV}.$$

The two differ by roughly six orders of magnitude. The relevant mechanism is chemical / condensed-matter, not nuclear.

## Conclusion

**F (E).**

## What this does not rule out

Condensed-matter effects on nuclear processes are not excluded as a class. **Electron screening in metals** is the physically defensible direction and is a measured effect; supercritical fluid chemistry is not.

## Refutation conditions

Reconsideration requires reproducible experiments demonstrating nuclear reaction products attributable to the proposed supercritical mechanism, with the branching ratios and product spectrum that mechanism would imply.

---

# 15. R6 — Fleming's law → $XYZ$

## Statement

The TTT $X,Y,Z$ axes derive from Fleming's left- and right-hand rules.

## Premises

1. Current $I$ is a true vector.
2. Force $F$ is a true vector.
3. Magnetic field $B$ is a pseudovector.
4. Left/right orientation is not an independent third physical law.

## Refutation

$B$, $I$ and $F$ do not transform identically under parity: $B$ does not change sign where $I$ and $F$ do. Three quantities with different transformation behaviour cannot serve as three equivalent axes of one ordinary 3-vector space.

Further, the left- and right-hand rules are not two independent laws; both restate $\vec F = q\vec v\times\vec B$. The finger assignment is a mnemonic, not a structure in nature.

## Conclusion

**F (A).**

## Where the real handedness is

Parity violation in the weak interaction (Wu 1957), the absence of right-handed neutrinos, and the V−A structure. That is the one place the universe is literally left-handed. A TTT chirality argument should attach there.

**Constructive note.** The awkwardness of pseudovectors is an artifact of three dimensions: rotations are properly **bivectors**, and only in 3D can the cross product impersonate a vector. Written in $\mathrm{Cl}(3)$ the anomaly disappears, and that machinery already exists in the v1.9 verification notes (vector/bivector decomposition unifying line and circle).

## Refutation conditions

Overturned only by a consistent representation in which the three quantities do serve as equivalent axes under the exact transformation rules TTT requires.

---

# 16. R7 — Five fingers as structural basis

## Statement

The number five derives from the human hand.

## Premises

1. Digit number varies across organisms.
2. Pentadactyly is not universal.
3. A structural theory must not rest on a contingent biological feature without a causal mechanism.

## Refutation

Early tetrapods had different digit counts — *Acanthostega* eight, *Ichthyostega* seven, *Tulerpeton* six. Pentadactyly was fixed later, in the Carboniferous. It is an evolutionary freeze, not a law. Therefore

$$\text{human pentadactyly} \nRightarrow \text{universal fivefold physical structure}.$$

Separately, the pentagonal bipyramid ($D_{5h}$) is achiral, so no chirality can be obtained from fivefold geometry alone.

## Conclusion

**F (E).**

## What survives

The hand contributes **handedness**, not fiveness — and the word *chirality* is itself from Greek χείρ, hand (Kelvin 1893). Chirality enters as a cyclic ordering, a sign, not as a shape. The fivefold structure is independently justified by P6 and does not need the hand.

The origin of fivefold structure in nature (maple leaves, echinoderm pentaradial symmetry) remains open and is a separate phenomenon from tetrapod digit count.

## Refutation conditions

Revivable only by demonstrating a causal biological-to-physical mechanism, not numerical resemblance.

---

# 17. O1 — Unit-conversion rule

*(absorbs U1 "energy scale of 125.25", U4 "density = 1", U5 "origin of 0.25", U6 "scale mechanism", and — added in v2.1 — the contested content of R2 and R3)*

## Why these are one problem

v1.0 listed four unknowns. They share a single cause: **TTT has no rule assigning physical units to its quantities.**

- U1 asked why 125.25 has an energy scale — that is the conversion rule.
- U4 asked whether $\rho=1$ may be assumed — that is the conversion rule stated as a normalisation.
- U5 asked where 0.25 comes from — the value cannot be evaluated without knowing what unit the 125 is in.
- U6 asked how particle and cosmological scales connect — that is the conversion rule applied across levels.

Two further items were relocated here in v2.1: **R2** ($648=501+147$) and the live part of **R3** (whether the overflow is 147 or 148). Both turn on the same question — see below.

Solving any one of these in isolation does not help; solving the conversion rule solves all six. Consequently **O1 is the single highest priority in the project**, and §28's list collapses accordingly.

## Current state

TTT distinguishes three kinds of quantity — **count**, **size**, **energy** — and this separation is legitimate: different quantities may take different values (124 / 125 / 125.25) without inconsistency. What is missing is the conversion between them.

TTT also distinguishes three counting levels: **tetrahedron (1) / O$\pi$O unit (4) / component (16)**, giving

$$162\ \text{tetrahedra} = 648\ \text{O}\pi\text{O} = 2592\ \text{components}.$$

The normalisation "size 1 ↔ energy 1" does not say *per what*. Per O$\pi$O the total is 648; per component it is 2592 — a factor of 4 difference, and earlier drafts differed by far more.

On 0.25 specifically: a volume-plus-surface reading fails, since $125^{2/3}=25$, a hundred times too large. Reading 0.25 as one component of a single four-component boundary object is consistent with O2 and is currently the only reading that survives.

## What R2 and R3 depend on

The two readings of the split are both arithmetically exact:

| Reading | Quantity | Space part | Overflow | Split |
|---|---|---:|---:|---|
| **Count** | tetrahedra × 4 | $125\times4=500$ | $648-500$ | $648=500+148$ |
| **Energy** | 125.25 at O$\pi$O granularity | $125.25\times4=501$ | $648-501$ | $648=501+147$ |

Neither is wrong on its own terms. **R2 is admissible if and only if 501 and 648 lie on the same scale** — that is, if the energy is measured per O$\pi$O unit rather than per component. That is exactly O1's question, which is why R2 belongs here and not under O3.

Consequences of the energy reading, which must be accepted together or not at all:

1. 147 is permitted ($147/4=36.75$ is only a problem for counts).
2. **"37 tetrahedra" is abandoned** — 37 is a count claim about an energy quantity, forbidden by the type rule.
3. 148 and the count reading go with it; the two splits cannot both be asserted.

Consequences of the count reading:

1. The split is $500+148$, and $148=37\times4$ holds exactly.
2. 125.25 loses its role in the split and must find its meaning elsewhere.
3. R2 stays refuted.

**This is a decision, not a discovery.** No new calculation will settle it; fixing the scale in O1 settles it. What is not permitted is leaving both in circulation and quoting whichever fits the paragraph — the failure v1.0's R2 section was reacting to.

## Level

**O.**

## Required proof

State explicitly

$$E=C_E\,Q, \qquad L=C_L\,Q$$

with $C_E, C_L$ derived independently — not fitted, and not chosen because they produce a known answer. Then derive

$$0.25=f(\text{TTT structural quantities})$$

from the boundary rules alone.

## Refutation conditions

**External form, and this is the decisive test in the entire document:**

Fix the conversion rule. Use it to map 125.25 onto a physical quantity **other than the Higgs mass**, chosen before the calculation. If that prediction misses the measured value beyond experimental uncertainty, O1 is refuted.

The restriction to a quantity other than $m_H$ is essential. $m_H = 125.20\pm0.11$ GeV is the number the conversion rule would be built to reproduce; reproducing it therefore tests nothing. A rule that predicts one further independent quantity is worth more than a hundred agreements with the number it was fitted to.

**Secondary condition.** If different physical systems require mutually incompatible conversion factors, the rule does not exist and O1 is negatively resolved.

**Condition specific to R2/R3.** Once the scale is fixed, one of the two splits above becomes unavailable. Whichever it is, every document in the project that uses the other must be corrected in the same commit — otherwise the theory has two arithmetics again.

---

# 18. O2 — Boundary component count

*(was U2)*

## Question

TTT writes both $O\pi O$ and $OO\pi O$. Is the leading $O$ in the second expression the same boundary as the one already inside, or an additional one? Four components or five?

## Derivation

**This has an answer, and it was reached on 2026-09-05.** A boundary is necessarily shared: the inside of one thing is the outside of another. The relevant identity is

$$\partial\partial=0$$

— the boundary of a boundary is zero, the identity Wheeler placed at the centre of the structure of gravitation (MTW).

Therefore the question "whose boundary is it, the particle's or the exterior's?" has no answer: there is one surface with two sides. A shared boundary must not be counted twice.

Hence

$$O_{\text{leading}} = O_{\text{internal}},$$

and $OO\pi O$ makes the boundary explicit without introducing a fifth component.

$$\boxed{\text{components} = 4}$$

Counting levels follow: 1 tetrahedron = 4 O$\pi$O = 16 components; $162 \times 16 = 2592$.

## Level

**B** — the derivation is valid but rests on the TTT-internal premise that its $O$ objects are boundaries in the sense $\partial$ applies to.

v1.0 listed this as U with a "preferred M2 candidate." The preference was already justified; leaving it unresolved understated the theory's position.

## Remaining work

Supply the formal object. Define each $O$ as an explicit element of a chain complex with a stated identity relation $O_i=O_j$ or $O_i\neq O_j$, and derive the count rather than asserting it. This is a modest, well-defined task and should be completed before O1, since O1's 0.25 depends on the answer being 4.

## Refutation conditions

**External form.** If the formal construction, once written, forces $O_i \neq O_j$ — that is, if the two objects cannot be identified without breaking the chain condition — then the count is five and every quantity built on the four-component reading, including 0.25, must be recomputed.

---

# 19. O3 — Structural count: 124, 125, or 128

*(absorbs U3 and the 37/38 parity issue. R2 and the live part of R3 were moved to **O1** in v2.1 — see §0.2(a).)*

## Question

Which count is fundamental?

$$124=31\times4, \qquad 125=5^{3}, \qquad 128=32\times4=2^{7}.$$

## Premises

1. Complete tetrahedral structures require multiples of four.
2. $125 = 4\times31+1$; 125 is not divisible by 4.
3. 128 also has the independent form $2^{7}$, which appears in the Alpha-V4 construction and matches $2^{5+2}$ in the vocabulary of P7.
4. A general fact: $n^{3}$ is divisible by 4 only for even $n$. For odd $n$ a remainder always exists — 1 when $n\equiv1 \pmod 4$, 3 when $n\equiv3$. For $n=5$ the remainder is exactly 1.

## Current state

The ordering

$$124<125<125.25<128$$

is numerically valid but does not by itself select a fundamental quantity.

Note that premise 4 explains *that* a remainder exists but does not single out five. Selecting $n=5$ is P6's job (crystallographic restriction). The two arguments do different work and are complementary: **the last generation is 5, and its remainder is exactly 1.**

## What was moved here

**From R4.** Whether the overflow is 37 or 38. The parity argument gives 38 (62 pairs fit in 125, one cell unpaired); the tetrahedral argument gives a remainder of 1 unit from 31 complete tetrahedra. These are different constraints and have not been reconciled.

**Boundary with O1.** O3 asks *how many objects there are*; O1 asks *what one unit is worth*. The count reading of the split ($500+148$) is an O3 answer; the energy reading ($501+147$) is an O1 answer. Keeping the two questions apart is what stops each from being used to settle the other — the circularity that put R2 back into play.

**Consequence.** Under three different count readings used within a single day (125 cells × 4 = 500 vs 648 → overflow 148; 125 = count of $O$; 125 = unit with 31 tetrahedra fitting vs 162 → overflow 131), **37 does not emerge from any of them.** Until the convention is fixed, no overflow number carries meaning.

## Level

**O.**

## Required proof

Derive one count from a TTT axiom, without selecting it because it yields a desired result. Then show that the alternative produces a contradiction. If both remain admissible, the count carries no information and cannot support anything built on it.

## Refutation conditions

**External form.** Whichever count is chosen must be attached to an observable through O1's conversion rule and compared. If the count cannot be attached to any observable, it is not a physical quantity and should be described as bookkeeping.

**Structural condition.** If a construction shows that the required structure cannot contain the chosen number at all, that candidate falls.

---

# 20. O4 — Fermionic representation

*(was U7)*

## Question

TTT associates the tetrahedral structure with four O$\pi$O units — an even count. Fermionic behaviour requires spinor representations and cannot be inferred from an even number.

## Premises

1. O$\pi$O is treated as a bosonic / spatial-energy unit.
2. A tetrahedral structure contains four such units.
3. Four is even.
4. Fermions require half-integer spin representations.

## Current state

$$\text{tetrahedron}=4\ \text{bosonic units}\ \nRightarrow\ \text{fermion}.$$

Counting parity is not statistics. The ledger has considered reading one O$\pi$O as a nucleon-level object instead, but the generation mechanism remains unresolved.

**Where the answer would come from.** P2 already identifies the relevant structure — the double cover, $U(2\pi)=-\mathbb{1}$ — so the ingredients are present. What is missing is a construction that produces a state transforming that way from TTT's own objects.

**Relevant prior finding.** The 2026-09-01 failure (the total transition operator telescoping to nothing) was traced to the operators being diagonal, hence commuting. Non-commutativity is exactly what $ijk=-1$ supplies. Any construction attempted here must be non-commutative or it will fail the same way.

## Level

**O.**

## Required proof

Construct a state $\psi$ from TTT structure satisfying

$$U(2\pi)\psi=-\psi,$$

with the sign emerging from the construction rather than inserted as an assumption, together with a consistent anticommutation structure.

## Refutation conditions

**External form.** If every representation constructible from TTT's stated objects is integer-spin, or if no consistent anticommutation structure exists over them, the fermionic programme is refuted and TTT cannot describe matter.

This is the sharpest structural test in the theory, because it is decidable by construction alone — no experiment is needed, only a proof or an impossibility argument.

---

# 21. Audit: Lie-operator document (2026-09-06)

Audit of *"Reference Transition Operators and the Lie Algebra $\mathfrak{gl}(3,\mathbb{R})$ in a 6-Dimensional Geometric State Space,"* reproduced independently (`ttt_lie_audit.py`).

## What holds

**M1–M2 = A.** The construction

$$T_i = I + \frac{\Delta_i\,p_i^{T}}{p_i^{T}p_i}$$

is the correct minimum-Frobenius-norm solution, and every published figure reproduces to the stated decimals: spectrum $\{1.62318319,\ 0.97131018,\ 0.99982298,\ 1,\ 1,\ 1\}$; singular values of $C$ equal to $(0.110126,\ 0.006588,\ 0.000032)$ with the first mode carrying 99.64%; $\operatorname{Tr}(G)=0.51527609$; distortion/swirl ratio $2.25637$.

The computation is sound. The interpretation is not.

## What fails

**M3, M4 = F (constructive artifacts).** The triple root at $\lambda=1$ and the 9-dimensional closure both reproduce for **all five random 4-vector test cases**. Performing three rank-1 updates in $\mathbb{R}^{6}$ necessarily leaves the orthogonal complement of $\mathrm{span}\{p_1,p_2,p_3\}$ invariant, and $\mathrm{span}\{u_iv_j^{T}\}$ is generically 9-dimensional. Neither has anything to do with polyhedra.

**M5 = F.** Rank-1 dominance of 99.64% is not significant. Random controls gave 77.9 / 81.3 / 92.7 / 97.6 / 98.3%.

**M6 = F (unit-dependent — most important).** The ratio $2.25637$ becomes 1.858 if the volume component is scaled by 10, 1.591 if by 1000, and 4.816 if $V,E,F$ are divided by 100. **A quantity that changes with the choice of units is not an invariant.** The cause is that the state vector places counts, solid angles, angles and volumes in the same column.

*This failure is repairable and should be repaired first.* Fix a dimensionless convention — divide $V,E,F$ by $V+E+F$, $\Omega$ by $4\pi$, $\delta$ by $2\pi$, $\mathcal{V}$ by the circumscribed-sphere volume — and recompute. The ratio then either survives or does not, and either outcome is informative.

**M7 = F.** The "conservation law" in $T_2$ (second row zero, $\text{Row}_3=-\text{Row}_1$) restates the input data ($E$ invariant, $\Delta V = -\Delta F$).

**M8, M9, M11 = F, and unrepaired since 2026-09-01.** In `golden_ratio_proofs` §1 the root is taken incorrectly (the positive solution of $x^{2}+x-1=0$ is $0.618=1/\varphi$, not $\varphi$); §5's optimisation has the unique solution $x=1/2$; `geometry_and_solution_space`'s claim that only five finite point systems satisfy $\sum v = 0$ is false — any centrally symmetric point system satisfies it.

**M10.** The "derivation" of the golden ratio in the axiomatisation is algebraically correct but axiom 6 *is* the golden-ratio equation. Nothing is derived.

**M12, M13 = C.** Fibonacci convergence assumes the limit exists (easily repaired). The fractal dimension $\log 3/\log\varphi$ has no stated basis.

## Assessment

The 2026-09-01 failure — total operator telescoping because diagonal matrices commute — has genuinely been fixed by rebuilding non-commutatively. That is progress.

But the *shape* of the error is unchanged. Previously: everything cancelled and nothing remained. Now: the same thing remains whatever is put in. Both are the same disease — **reading a consequence of the construction as a discovery about the content.**

The diagnostic is cheap and should be run before any structural claim: substitute random inputs. If the result persists, it is a property of the construction.

---

# 22. Audit: Unified Geometric Table (2026-09-06)

Audit of *TTT-Physics Grand Synthesis v1.0*, running the bundled `src/ttt_17_mass_ratios.py` unmodified.

**G1 = F.** "Reproduces $m_s, m_c, m_b, m_t$" does not hold. **Seven of seventeen masses are off by 55–99%**: tau −74.19%, charm −55.75%, bottom −68.35%, top −96.08%, and W/Z/H together −99.12%. The values 3477 / 2485 / 8180 / $3.4\times10^{5}$ in the "ratio $m_i/m_e$" column are **measured values, not model outputs** — measured values placed in a prediction column.

**G2 = implementation bug.** W, Z and H fail identically because all three scale with `v_ratio`. The comment says $v/m_e \approx 481450$, but the expression $\frac{1}{\alpha\sqrt2\pi}\cdot6\pi^{3}$ returns **5738** — off by a factor of 84. The true value is $246220/0.511 = 481838$, so the intent was right and the implementation was wrong.

**G3 = misuse, with a correct version available.** The tau is implemented as $m_\tau = m_\mu(1+\sqrt2\cos(2\pi/9))^{2}$, a misapplication of Brannen's expression (which supplies all three generations at $n=0,1,2$, not a $\mu\to\tau$ multiplier). Solving **Koide's relation**

$$m_e+m_\mu+m_\tau=\frac{2}{3}\left(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau}\right)^{2}$$

for $m_\tau$ correctly gives $1776.97$ MeV against $1776.86\pm0.12$ measured.

**G4.** Of the four rows that agree, muon (0.00%), up (−0.53%) and down (−0.02%) each contain hand-placed coefficients (−6.788, ×2.58, +$\pi$×1.57). The only row with no free number is strange, $6\pi^{3}(1-\alpha_s/2\pi)$, at −0.13% — but $m_s = 93.4^{+8.6}_{-3.4}$ MeV carries ~10% experimental uncertainty and therefore cannot test anything to 0.13%.

**G5 = F.** "No free parameters" is false. The inputs 2.58, 1.57, −6.788, $\div\sqrt3$, $\times\sqrt2$, −0.08, $\div\sqrt2$, $\sqrt{2.427}$ and $\sin^{2}\theta_W$ amount to at least nine hand-placed numbers for seventeen masses.

**G6 = O (requires action).** Sections A, C, D, E, F and G are **correct summaries of existing literature** — RS1, the SO(5)/SO(4) composite Higgs, Coleman–Weinberg, Weinberg sum rules, MCHM, LHC limits — and are not TTT results. Only sections B and H originate with TTT. Six of eight sections of a document titled "Grand Synthesis" are other people's work. **Sources must be cited**; without citation this reads as plagiarism.

**G7 = minor.** With $k\pi R\approx39.14$, $e^{-k\pi R}=1.0\times10^{-17}$, while the table gives $2\times10^{-17}$.

---

# 23. Audit: post-correction retest (2026-09-06)

G2 and G3 were implementation errors, not theory errors, so they were repaired before judging the whole (`ttt_mass_refit_test.py`).

## Results after repair

| Row | Before | After | Method |
|---|---:|---:|---|
| tau | −74.19% | **+0.0061%** (0.9σ) | Koide's relation solved for $m_\tau$ → 1776.9690 MeV |
| W | −99.12% | **−0.18%** | $v/m_e = 481840$ input, $m_W=gv/2$ |
| Z | −99.12% | **+0.35%** | $m_Z = m_W/\cos\theta_W$ |

## The decisive finding

**Every row that was repaired stopped being TTT.**

The tau agrees because Koide's relation (1981) agrees. W and Z agree because $v$ and $\sin^{2}\theta_W$ were supplied as inputs to tree-level Standard Model formulae. The Higgs has no derivation at all.

> **The more the file is corrected, the smaller TTT's contribution becomes.** Every improved row improved by being replaced with established physics.

## Null control

Charm, bottom and top were deliberately **not** fitted — not because it is hard, but because it takes minutes. An exhaustive search over 882 combinations of $6\pi^{n}$ with $\{1,\sqrt2,\sqrt3,2,\pi,\varphi,\ldots\}$ and $(1\pm k\alpha_s/\pi)$ reaches strange $=6\pi^{2}\times\pi$, charm $=6\pi^{4}\times\sqrt2\pi$, bottom $=6\pi^{5}\times\sqrt2\pi$ and tau $=6\pi^{6}/\sqrt3$, all within 1% (only top is unreachable).

**Control:** of 2000 random targets drawn log-uniformly from 100 to 400000, **1438 (71.9%) are reachable within 1%** using the same vocabulary.

$$\boxed{\text{Hit rate on random targets} = 71.9\%}$$

**Consequence: in this vocabulary, hitting a target is not evidence.** This is the mass-ratio version of the 2026-09-02 result (26% of two-digit values, against a 26.4% control), and the wider range of magnitudes makes the reachability higher still.

## Verdict

After repair, one row survives with no hand-placed constant (strange, −0.13%), and it survives inside a 71.9% reachability band with a 10% experimental uncertainty. **Nothing remains as evidence.**

## The one defensible continuation

Abandon mass-ratio fitting and concentrate on **Koide's relation**. It has been unexplained since 1981, it is a *relation* rather than a fit, and with a single target the degrees-of-freedom objection does not apply.

**The condition is strict and non-negotiable: derive why $\theta_k = 2\pi/9$, do not restate the relation.** Until that is done, the tau's +0.01% is Koide's achievement, not TTT's.

---

# 24. Global logical status

The statements do not share a single proof status. They occupy three layers.

## Layer A — Mathematical structure

$\pi=-1$ under its stated premises; $\kappa=1/r$; the crystallographic restriction; $V(n)=n+2$; the arithmetic refutations R1, R3, R4.

Evaluable by ordinary mathematics. **Two of these are definitions ($\kappa=1/r$, $\pi=-1$), three are arithmetic (R1, R3, R4), and the two genuine theorems — the crystallographic restriction and Euler's formula — are both borrowed.**

## Layer B — Physical interpretation

Boundary as threshold; emission at structural birth; mass and escape; the generation limit; centre/boundary duality; fermionic generation.

Each requires

$$\boxed{\text{TTT mathematical structure}\ \longrightarrow\ \text{physical observable}}$$

and the bridge must itself be derived. **O1 is that bridge**, and it does not currently exist. This is why every Layer B entry sits at C.

## Layer C — Empirical prediction

A theory becomes strong when it produces

$$\boxed{\text{axioms}\rightarrow\text{mathematical quantity}\rightarrow\text{physical unit}\rightarrow\text{numerical prediction}\rightarrow\text{null control}\rightarrow\text{experiment}}$$

without inserting the known answer during the derivation.

**Present status of Layer C.** The three live numerical results — $m_H = 125.25$ GeV, the 125 MeV medium gap, and the 2.24 meV / 88.1 μm vacuum scale — do **not** pass through the middle of this chain. They come from the $\alpha$-expression series, a fit to the deuteron $Q$-value, and a self-consistency condition respectively.

The honest reading of that is structural, not merely negative: **a short path (definition → physical mapping → prediction) is working, while the long path's middle section failed on 2026-09-01.** Consolidating the short path first and treating the middle as a separate track is the better order of work, whatever the roadmap says.

---

# 25. Required standard for future TTT proofs

Every new claim must follow this chain. Two steps are new in v2.0 and are marked.

```text
Definition
    ↓
Premises
    ↓
Mathematical derivation
    ↓
TTT-specific bridge
    ↓
Unit-conversion rule            ← NEW (this is O1; a claim that skips it is not a physical claim)
    ↓
Physical quantity
    ↓
Numerical prediction
    ↓
Null control                    ← NEW (see §26)
    ↓
Experimental comparison
    ↓
Falsification condition
```

A numerical coincidence alone is insufficient. Every claim must distinguish

$$\boxed{\text{derived}} \quad \boxed{\text{assumed}} \quad \boxed{\text{observed}} \quad \boxed{\text{fitted}}$$

and say which of the four each number in it is.

**Additional requirement (from G6).** Any section summarising external work must cite it. A document that presents standard results without attribution is not merely impolite; it makes the theory's own contribution unmeasurable, which defeats the purpose of this file.

---

# 26. The null-control requirement

v1.0 stated the right principle and gave no way to enforce it. This section is the instrument.

## Procedure

Before any claim of numerical agreement:

1. **Define the vocabulary.** List every operation and constant the derivation is permitted to use ($6\pi^{n}$, $\sqrt2$, $\varphi$, $\alpha$, $\ldots$).
2. **Fix the target in advance.** Write down what is being predicted before computing.
3. **Run the control.** Generate a few thousand random targets on the same logarithmic range and count how many the vocabulary reaches within the same tolerance.
4. **Report the hit rate alongside the result.** Always. A 0.1% agreement means nothing if the control hit rate is 70%.
5. **Compare against experimental uncertainty.** An agreement tighter than the measurement's own error bar is not a stronger result; it is an untested one.

## Established control values

| Domain | Date | Control hit rate |
|---|---|---:|
| Two-digit physical constants | 2026-09-02 | 26.4% (claim: 25.7%) |
| Mass ratios, $6\pi^n$ vocabulary | 2026-09-06 | **71.9%** |

## Rule

> **A result whose hit rate under the null control is not reported has not been tested.**

This applies to TTT's successes as strictly as to its failures. It is what makes the file's refutations credible.

---

# 27. Principles of scientific honesty

> **A result is not promoted from coincidence to derivation because it agrees with an observed value.**

> **A mathematically elegant structure is not promoted to physical law without a testable bridge.**

> **A failed numerical decomposition is recorded as rejected, not repaired after the fact.**

Three further principles, added in v2.0 from what the audits taught:

> **A consequence of the construction is not a discovery about the content.** Before any structural claim, substitute random inputs. If the result persists, it is an artifact. (§21)

> **A quantity that changes when the units change is not an invariant.** (§21, M6)

> **A correction that improves agreement by replacing TTT with established physics has reduced the theory, not improved it.** Track which rows are TTT's after every repair. (§23)

---

# 28. Next proof targets

The priority list collapses relative to v1.0, because four of its seven unknowns were one problem.

### Priority 0 — O2 (small, and blocks O1)

Write the formal chain-complex definition of the $O$ objects and fix the component count at 4. A few days' work; O1's 0.25 cannot be evaluated until it is done.

### Priority 1 — O1 (the whole of the old priorities 1, 2, 3 and 5)

Establish the unit-conversion rule. Then predict **one independent quantity other than $m_H$** and compare. Nothing else in the theory can be tested until this exists. Fixing the scale simultaneously decides R2 and the 147/148 question, and therefore whether "37 tetrahedra" survives at all.

### Priority 2 — Repair M6

Fix the dimensionless convention in the Lie-operator document and recompute the distortion/swirl ratio. Cheap, and either outcome is informative.

### Priority 3 — O3

Derive 124 or 128 from an axiom and show the alternative contradicts. This also settles the 37/38 parity issue. (R2 and the 147/148 question are settled by O1, not here — see §0.2(a).)

### Priority 4 — O4

Construct a representation with $U(2\pi)\psi=-\psi$ using non-commuting operators.

### Priority 5 — P6

Turn the crystallographic restriction into an explicit map from rotational order to generation, written down before comparing with $N_\nu = 2.9840 \pm 0.0082$.

### Priority 6 — Koide

Derive $\theta_k = 2\pi/9$. Single target, no degrees-of-freedom objection, unexplained since 1981. The highest-value item in the list if it can be done — and worth nothing if the relation is merely restated.

### Housekeeping — G6

Add citations to the Grand Synthesis for sections A, C, D, E, F, G. Do this before any further distribution of that document.

---

# 29. Final status

At present TTT contains:

- mathematically valid internal structures, of which the theorem-level ones are borrowed;
- **no theorem proven by TTT itself**;
- ten explicit refutations of its own earlier proposals (R1, R3–R7; M3–M11 collectively; G1, G5; N1);
- physically meaningful hypotheses at Layer B, all currently blocked on the same missing bridge;
- three numerical results reached by a short path that bypasses the theory's own machinery;
- and four unresolved problems, one of which (O1) gates the rest.

The defensible position is therefore:

$$\boxed{
\begin{array}{c}
\text{TTT is a research framework with partially proven mathematics,}\\
\text{partially supported physical interpretations,}\\
\text{and an unbuilt bridge between them.}
\end{array}
}$$

It must **not** be described as an experimentally established fundamental physical theory.

**What has actually improved between v1.0 and v2.1** is not the theory's standing — the audits lowered it — but its testability. Six unknowns became one named obstacle with an external refutation condition; a rejection that rested on an unresolved premise was withdrawn; and the project acquired a null control, which is the first instrument it has had for telling a result from a coincidence.

v2.1 also demonstrates the intended use of this file: it was v2.0's own type rule — counts and energies are different quantities — that exposed v2.0's misattribution of R2. **A ledger that catches its author's errors is doing its job.** Corrections are recorded here rather than applied silently, for the same reason failed decompositions are kept: a document that quietly repairs itself cannot be audited.

The purpose of this document is to make the remaining path from mathematical structure to physical prediction explicit and falsifiable. On that measure, the honest summary is that the path is now visible and shorter than it looked, and that nothing has yet travelled it.
