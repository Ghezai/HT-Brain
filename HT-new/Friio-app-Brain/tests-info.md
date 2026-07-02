## Tests inside the app

Friio has unit-test setup and actual tests.

Webshop: has Vitest configured in [package.json](E:/utv/Friio/src/webshop/application/package.json), but I did not find actual .test / .spec files under src/webshop/application.

Plow backoffice: has Vitest and actual utility tests:[invertIf.spec.ts](E:/utv/Friio/src/plow-backoffice/app/utils/__test__/invertIf.spec.ts)
[applyFiltersFromQueryParams.spec.ts](E:/utv/Friio/src/plow-backoffice/app/utils/__test__/applyFiltersFromQueryParams.spec.ts)

NPM shared libraries: have Jest-style tests:friio-multi-organizations/src/tests/*
friio-app-roles/src/tests/Roles.test.ts

.NET backend: has xUnit test projects:[Platform.API.Tests.csproj](E:/utv/Friio/src/platform/src/API/Platform.API.Tests/Platform.API.Tests.csproj)
Platform.BuildingBlocks.Maps.Tests
Platform.Integrations.GisCloud.Tests

So the answer is: yes, but coverage is uneven. Backend has a lot of xUnit tests, plow-backoffice has a small number of Vitest unit tests, shared libraries have tests, and webshop currently looks configured for Vitest but without obvious test files.

The main backend xUnit tests are here:
[Platform.API.Tests](E:/utv/Friio/src/platform/src/API/Platform.API.Tests)
Test project: [Platform.API.Tests.csproj](E:/utv/Friio/src/platform/src/API/Platform.API.Tests/Platform.API.Tests.csproj)
Examples:[HealthTests.cs](E:/utv/Friio/src/platform/src/API/Platform.API.Tests/HealthTests.cs)
[CabinsTests.cs](E:/utv/Friio/src/platform/src/API/Platform.API.Tests/Cabins/CabinsTests.cs)
[CabinManagementTests.cs](E:/utv/Friio/src/platform/src/API/Platform.API.Tests/Cabins/CabinManagementTests.cs)
[CustomerPresenceTests.cs](E:/utv/Friio/src/platform/src/API/Platform.API.Tests/CustomerPresenceTests.cs)
[PlowingInstructionsTests.cs](E:/utv/Friio/src/platform/src/API/Platform.API.Tests/PlowingInstructionsTests.cs)
[PlatformUserTests.cs](E:/utv/Friio/src/platform/src/API/Platform.API.Tests/PlatformUserTests.cs)

There are also smaller backend xUnit test projects here:
[Platform.BuildingBlocks.Maps.Tests](E:/utv/Friio/src/platform/src/BuildingBlocks/Platform.BuildingBlocks.Maps.Tests)
[GeometryServiceTests.cs](E:/utv/Friio/src/platform/src/BuildingBlocks/Platform.BuildingBlocks.Maps.Tests/GeometryServiceTests.cs)
[Platform.Integrations.GisCloud.Tests](E:/utv/Friio/src/platform/src/Integrations/Platform.Integrations.GisCloud.Tests)
[GeometryServiceTests.cs](E:/utv/Friio/src/platform/src/Integrations/Platform.Integrations.GisCloud.Tests/GeometryServiceTests.cs)