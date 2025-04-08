const fs = require('node:fs/promises');
const path = require('node:path');

// Configuration object for exclusions
const config = {
  rootDir: process.cwd(), // Current working directory
  excludeDirs: [
    'venv',           // Virtual environment
    '__pycache__',    // Python bytecode cache
    '.git',          // Git repository
    '.vscode',       // VS Code settings
    'node_modules',  // Node.js dependencies (if any)
    'migrations',    // Flask-Migrate migrations
    'instance',      // Flask instance folder
    'static/uploads' // User-uploaded files (optional)
  ],
  excludeFiles: [
    '.gitignore',
    '.env',
    '*.db',           // SQLite database files (e.g., app.db, arte_moderno.db)
    'bundled-project.txt', // Output from your bundleFiles.js
    'files-tree.txt', // Another potential output file
    '*.log',          // Log files
    'requirements.txt' // Optional: exclude if you don’t want it listed
  ]
};

// Check if a directory should be traversed
const shouldIncludeDir = (dirPath) => {
  const baseName = path.basename(dirPath);
  return !config.excludeDirs.includes(baseName);
};

// Check if a file should be included (basic wildcard support)
const shouldIncludeFile = (filePath) => {
  const baseName = path.basename(filePath);
  return !config.excludeFiles.some(pattern => {
    if (pattern.includes('*')) {
      const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
      return regex.test(baseName);
    }
    return pattern === baseName;
  });
};

// Recursive function to list files
async function listFiles(dir) {
  const fileList = [];
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.relative(config.rootDir, fullPath);

      if (entry.isDirectory() && shouldIncludeDir(fullPath)) {
        const subFiles = await listFiles(fullPath);
        fileList.push(...subFiles);
      } else if (entry.isFile() && shouldIncludeFile(fullPath)) {
        fileList.push(relativePath);
      }
    }
  } catch (err) {
    console.error(`Error reading directory ${dir}:`, err);
  }
  return fileList;
}

// Main function to execute the listing
async function generateFileList() {
  console.log('Generating file list...');
  const files = await listFiles(config.rootDir);

  if (files.length === 0) {
    console.log('No files found.');
    return;
  }

  // Sort files alphabetically for consistency
  files.sort();

  // Print the list
  console.log('\nList of files:');
  files.forEach(file => console.log(file));

  // Optional: Write to a file
  const outputPath = path.join(config.rootDir, 'file-list.txt');
  await fs.writeFile(outputPath, files.join('\n'), 'utf8');
  console.log(`\nFile list saved to ${outputPath}`);
}

// Run the script with error handling
(async () => {
  try {
    await generateFileList();
  } catch (err) {
    console.error('Error generating file list:', err);
    process.exit(1);
  }
})();