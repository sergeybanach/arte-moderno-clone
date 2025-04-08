const fs = require('node:fs/promises');
const path = require('node:path');

// Configuration object for customization
const config = {
  rootDir: process.cwd(),
  outputFile: 'bundled-project.txt',
  includeExtensions: [
    '.js', '.jsx', '.css', '.html', '.py', '.json', '.txt', '.md', '.ini', '.mako', // Text-based extensions
  ],
  excludeDirs: [
    'node_modules',
    'venv',           // Virtual environment
    '__pycache__',    // Python bytecode cache
    '.git',          // Git repository
    '.vscode',       // VS Code settings
    'instance',      // Flask instance folder
    // 'migrations',    // Flask-Migrate migrations (optional: remove if you want migration scripts)
  ],
  excludeFiles: [
    // '.env',           // Environment files with secrets
    // '.gitignore',
    'bundled-project.txt', // Prevent self-inclusion
    'app.db',         // SQLite database
    'arte_moderno.db', // Another SQLite database
    'files-tree.txt', // Exclude other generated outputs
    'full-list.txt',
    'list.txt',
  ],
  excludeBinaryExtensions: [
    '.jpg', '.jpeg', '.png', '.gif', '.webp', // Image files
    '.db',          // Database files
    '.svg',         // SVG can be text, but often treated as binary in this context
  ],
};

// Check if a file should be included
const shouldIncludeFile = (filePath) => {
  const ext = path.extname(filePath).toLowerCase();
  const baseName = path.basename(filePath);

  // Exclude if it's in excludeFiles or has a binary extension
  if (config.excludeFiles.includes(baseName) || config.excludeBinaryExtensions.includes(ext)) {
    return false;
  }

  // Include only if it has an allowed text-based extension
  return config.includeExtensions.includes(ext);
};

// Check if a directory should be traversed
const shouldIncludeDir = (dirPath) => {
  const baseName = path.basename(dirPath);
  return !config.excludeDirs.includes(baseName);
};

// Recursive function to collect files with content
async function collectFiles(dir) {
  const results = [];
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    // Process entries in parallel for performance
    await Promise.all(
      entries.map(async (entry) => {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && shouldIncludeDir(fullPath)) {
          const subFiles = await collectFiles(fullPath);
          results.push(...subFiles);
        } else if (entry.isFile() && shouldIncludeFile(fullPath)) {
          try {
            const content = await fs.readFile(fullPath, 'utf8');
            results.push({
              filePath: path.relative(config.rootDir, fullPath),
              content: content.trimEnd(), // Trim content to save memory
            });
          } catch (err) {
            console.error(`Error reading file ${fullPath}:`, err);
          }
        }
      })
    );
  } catch (err) {
    console.error(`Error reading directory ${dir}:`, err);
  }
  return results;
}

// Main function to bundle files
async function bundleProject() {
  console.log('Collecting files...');
  const files = await collectFiles(config.rootDir);

  if (files.length === 0) {
    console.log('No files found to bundle.');
    return;
  }

  console.log(`Found ${files.length} files. Bundling into ${config.outputFile}...`);

  // Use a stream for writing large files efficiently
  const outputPath = path.join(config.rootDir, config.outputFile);
  const stream = (await fs.open(outputPath, 'w')).createWriteStream();

  for (const file of files) {
    stream.write(`### ${file.filePath} ###\n${file.content}\n\n`);
  }

  stream.end();
  console.log(`Successfully bundled project into ${config.outputFile}`);
}

// Error handling wrapper
(async () => {
  try {
    await bundleProject();
  } catch (err) {
    console.error('Error bundling project:', err);
    process.exit(1);
  }
})();