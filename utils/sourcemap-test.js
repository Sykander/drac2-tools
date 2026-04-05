const prodSourceMap = require('./sourcemap.prod.json');
const devSourceMap = require('./sourcemap.dev.json');

console.log(
  '❓ Checking Production Sourcemap includes everything from Development Sourcemap',
);
console.log('❓ ALIASES CHECK');

const { aliases, snippets, gvars } = {
  aliases: [],
  snippets: [],
  gvars: [],
  ...devSourceMap,
};
const {
  aliases: prodAliases,
  snippets: prodSnippets,
  gvars: prodGvars,
} = { aliases: [], snippets: [], gvars: [], ...prodSourceMap };

const compareSubAliases = (devSubAliases, prodSubAliases) =>
  devSubAliases.every((devSubAlias) => {
    const prodSubAlias = prodSubAliases.find(
      ({ name }) => devSubAlias.name === name,
    );

    if (!prodSubAlias) {
      console.log(
        `❌ ${devSubAlias.name} SUB ALIAS doesn't have a matching sub alias in production.`,
      );
      return false;
    }

    if (devSubAlias.file !== prodSubAlias.file) {
      console.log(
        `❌ ${devSubAlias.name} SUB ALIAS has a different file in production.`,
      );
      return false;
    }

    if (devSubAlias.sub_aliases) {
      if (!prodSubAlias.sub_aliases) {
        console.log(
          `❌ ${devSubAlias.name} SUB ALIAS has sub aliases in dev but not production`,
        );
        return false;
      }

      const subAliasesMatch = compareSubAliases(
        devSubAlias.sub_aliases,
        prodSubAlias.sub_aliases,
      );

      if (!subAliasesMatch) {
        console.log(
          `❌ ${devSubAlias.name} SUB ALIAS has different sub aliases in production`,
        );
        return false;
      }
    }

    return true;
  });

const aliasesMatch = aliases.every((devAlias) => {
  const prodAlias = prodAliases.find(({ name }) => devAlias.name === name);

  if (!prodAlias) {
    console.log(
      `❌ ${devAlias.name} ALIAS doesn't have a matching alias in production`,
    );
    return false;
  }

  // Check files match
  if (devAlias.file !== prodAlias.file) {
    console.log(`❌ ${devAlias.name} ALIAS has a different file in production`);
    return false;
  }

  // check sub aliases match
  if (devAlias.sub_aliases) {
    if (!prodAlias.sub_aliases) {
      console.log(
        `❌ ${devAlias.name} ALIAS has sub aliases in development but not production`,
      );
      return false;
    }

    const subAliasesMatch = compareSubAliases(
      devAlias.sub_aliases,
      prodAlias.sub_aliases,
    );

    if (!subAliasesMatch) {
      console.log(
        `❌ ${devAlias.name} ALIAS sub aliases don't match in production`,
      );
      return false;
    }
  }

  return true;
});

if (!aliasesMatch) {
  console.log('❌ ALIASES CHECK FAILED');
  process.exit(1);
}

console.log('✅ ALIASES CHECK PASSED');

console.log('❓ SNIPPETS CHECK');

const snippetsMatch = snippets.every((devSnippet) => {
  const prodSnippet = prodSnippets.find(({ name }) => devSnippet.name === name);

  if (!prodSnippet) {
    console.log(
      `❌ ${devSnippet.name} SNIPPET doesn't have a matching snippet in production`,
    );
    return false;
  }

  // Check files match
  if (devSnippet.file !== prodSnippet.file) {
    console.log(
      `❌ ${devSnippet.name} SNIPPET has a different file in production`,
    );
    return false;
  }

  return true;
});

if (!snippetsMatch) {
  console.log('❌ SNIPPETS CHECK FAILED');
  process.exit(1);
}

console.log('✅ SNIPPETS CHECK PASSED');

console.log('❓ GVARS CHECK');

const matchesInProd = prodGvars.filter(
  ({ id }, index, src) =>
    index != src.findIndex(({ id: testId }) => testId === id),
);

if (matchesInProd.length) {
  console.log(
    `❌ Multiple GVARS have ID ${matchesInProd[0].id} in Production.`,
  );
  process.exit(1);
}

const gvarsMatch = gvars.every((devGvar) => {
  const prodGvar = prodGvars.find(({ name }) => devGvar.name === name);

  const matchesIdInDev = gvars.filter(({ id }) => id === devGvar.id);

  if (matchesIdInDev.length > 1) {
    console.log(
      `❌ ${devGvar.name} GVAR and ${matchesIdInDev[1].name} GVAR IDs are the same in Development`,
    );
    return false;
  }

  if (!prodGvar) {
    console.log(
      `❌ ${devGvar.name} GVAR doesn't have a matching gvar in production`,
    );
    return false;
  }

  if (devGvar.id === prodGvar.id) {
    console.log(`❌ ${devGvar.name} GVAR has the same ID in production`);
    return false;
  }

  // Check files match - exclude env file as these shouldn't match
  if (devGvar.file !== prodGvar.file && devGvar.name !== 'env') {
    console.log(`❌ ${devGvar.name} GVAR has a different file in production`);
    return false;
  }

  return true;
});

if (!gvarsMatch) {
  console.log('❌ GVARS CHECK FAILED');
  process.exit(1);
}

console.log('✅ GVARS CHECK PASSED');

console.log('✅ Development and Production sourcemaps match');
