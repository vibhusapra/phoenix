import { expect, test } from "@playwright/test";
import { randomUUID } from "crypto";

// This e2e test verifies creating a project via the UI without tracing.
// Flow: login -> open New Project -> select "No Tracing" tab -> fill form -> submit -> verify redirect and listing

test.beforeEach(async ({ page }) => {
  await page.goto(`/login`);
  await page.getByLabel("Email").fill("member@localhost.com");
  await page.getByLabel("Password").fill("member123");
  await page.getByRole("button", { name: "Log In", exact: true }).click();
  await page.waitForURL("**/projects");
});

test("Create project without tracing", async ({ page }) => {
  const projectName = `proj-${randomUUID().slice(0, 8)}`;

  // Open the New Project modal from the Projects page header
  await expect(page.getByRole("button", { name: "New Project" })).toBeVisible();
  await page.getByRole("button", { name: "New Project" }).click();

  // Switch to the "No Tracing" tab
  await page.getByRole("tab", { name: "No Tracing" }).click();

  // Fill the project form
  await page.getByRole("textbox", { name: "Project Name" }).fill(projectName);
  // Description optional; provide a short one
  await page.getByRole("textbox", { name: "Description" }).fill("E2E created project");

  // Submit the form
  await page.getByRole("button", { name: "Create Project" }).click();

  // Expect redirect to the project page: /projects/:id
  await page.waitForURL(/\/projects\/.+$/);

  // Navigate back to projects list and verify the new project appears
  await page.goto("/projects");
  await expect(page.getByRole("link", { name: projectName })).toBeVisible({ timeout: 60000 });
});
