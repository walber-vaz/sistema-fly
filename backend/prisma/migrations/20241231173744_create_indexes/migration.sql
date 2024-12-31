-- CreateIndex
CREATE INDEX "tb_users_lastLogin_idx" ON "tb_users"("lastLogin");

-- CreateIndex
CREATE INDEX "tb_users_failedLoginAttempts_idx" ON "tb_users"("failedLoginAttempts");

-- CreateIndex
CREATE INDEX "tb_users_permissions_granted_idx" ON "tb_users_permissions"("granted");
