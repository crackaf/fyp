// basic .eslintrc.js compatible with react prettier and typescript
module.exports = {
  // Specifies the ESLint parser for TypeScript
  parser: "@typescript-eslint/parser",
  extends: [
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:prettier/recommended",
    "prettier",
  ],
  settings: {
    "import/resolver": {
      node: {
        paths: ["./src"],
        extensions: [".js", ".jsx", ".ts", ".tsx"],
      },
    },
    react: {
      version: "detect",
    },
  },
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  plugins: ["@typescript-eslint", "react", "prettier"],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    // Allows for the parsing of modern ECMAScript features
    ecmaVersion: 2018,
    // Allows for the use of imports
    sourceType: "module",
  },
  rules: {
    "no-console": ["warn", { allow: ["info", "warn", "error", "debug"] }],
    "no-plusplus": 0,
    "prefer-destructuring": ["warn", { object: true, array: false }],
    "no-underscore-dangle": 0,
    "import/prefer-default-export": 0,
    "no-param-reassign": [
      "error",
      { props: true, ignorePropertyModificationsFor: ["state", "memo"] },
    ],
    "react/require-default-props": 0,
    "no-nested-ternary": 0,
    "max-classes-per-file": 0,

    "@typescript-eslint/no-var-requires": "off",
    // Disable prop-types as we use TypeScript for type checking
    "react/prop-types": "off",
    "@typescript-eslint/explicit-function-return-type": "off",
    // Enable prettier rules
    "prettier/prettier": "error",
    // interface start with capital I
    "@typescript-eslint/interface-name-prefix": "off",
    // allow "any" as type
    "@typescript-eslint/no-explicit-any": "off",
    // allow @ts-ignore for testing purposes
    "@typescript-eslint/ban-ts-ignore": "off",
  },
};
