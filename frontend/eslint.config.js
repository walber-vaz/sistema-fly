import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import tseslint from 'typescript-eslint';
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended';
import prettier from 'eslint-plugin-prettier';
import simpleImportSort from 'eslint-plugin-simple-import-sort';
import pluginQuery from '@tanstack/eslint-plugin-query';
import tailwind from 'eslint-plugin-tailwindcss';

export default tseslint.config(
    { ignores: ['dist', 'node_modules', 'yarn.lock'] },
    {
        extends: [
            js.configs.recommended,
            eslintPluginPrettierRecommended,
            ...tailwind.configs['flat/recommended'],
            ...tseslint.configs.recommended,
        ],
        files: ['**/*.{ts,tsx}'],
        languageOptions: {
            ecmaVersion: 2020,
            globals: globals.browser,
        },
        settings: {
            react: {
                version: 'detect',
            },
        },
        plugins: {
            'react-hooks': reactHooks,
            'react-refresh': reactRefresh,
            'simple-import-sort': simpleImportSort,
            '@tanstack/query': pluginQuery,
            prettier,
        },
        rules: {
            ...reactHooks.configs.recommended.rules,
            'simple-import-sort/imports': 'error',
            'simple-import-sort/exports': 'error',
            'prettier/prettier': 'error',
            quotes: ['error', 'single'],
            semi: ['error', 'always'],
            'max-len': [
                'error',
                {
                    code: 80,
                    ignoreUrls: true,
                    ignoreStrings: true,
                    ignoreTemplateLiterals: true,
                    ignoreComments: true,
                    ignoreRegExpLiterals: true,
                    ignoreTrailingComments: true,
                },
            ],
            'react-hooks/rules-of-hooks': 'off',
            'react-refresh/only-export-components': [
                'warn',
                { allowConstantExport: true },
            ],
        },
    },
);
