# QSOBuilder Punch List

The Architect sets order in `taskchain.md`; QSOBuilder executes one bounded, testable item at a time.

## Immediate
- [ ] Establish a reproducible repository health baseline.
- [ ] Verify the bounded multi-object experiment is runnable and preserves freeze points, ethics, provenance, and size limits.
- [ ] Define the QSO object payment-capability schema without enabling uncontrolled transfers.
- [ ] Add test fixtures for direct payment, percentage splits, royalties, validator rewards, escrow milestones, pooled treasury, and fiat/stablecoin adapters.
- [ ] Keep simulation/testnet behavior distinct from production settlement.

## Quality Gates
- [ ] Deterministic tests and rollback path.
- [ ] No generated code is executed without validation.
- [ ] Payment intent, authorization, distribution rules, receipts, and audit records are explicit.
