/*!
 * @Author: CPS
 * @email: 373704015@qq.com
 * @Date: 2023-01-30 22:32:44.617352
 * @Last Modified by: CPS
 * @Last Modified time: 2023-01-30 22:32:44.617352
 * @Projectname
 * @file_path "D:\CPS\MyProject\test\cps-scripts\markdown"
 * @Filename "文件名注入为标题.ts"
 * @Description: 为每个md文件注入一个标题，标题根据文件名而定
 */

import fsp from 'fs/promises';
import path from 'path';
import { glob, IOptions } from 'glob';
import { cursorTo } from 'readline';

/**
 * @Description - {description}
 *
 * @param {number} currtDeep=0  - {description}
 * @param {number} maxDeep=100  - {description}
 * @param {string} dirPath      - {description}
 *
 * @returns {} - {description}
 *
 */
async function walk({
  dirPath,
  currtDeep = 0,
  maxDeep = 100,
}: {
  dirPath: string;
  currtDeep?: number;
  maxDeep?: number;
}) {
  if (currtDeep > maxDeep) return console.log('超过最大递归次数');

  dirPath = path.resolve(dirPath);
  const dirList = await fsp.readdir(dirPath);
  console.log('dirList: ', dirList);

  dirList.forEach(async eachFile => {
    const fullPath = path.join(dirPath, eachFile);
    const fileInfo = await fsp.stat(fullPath);
    const dirname = path.dirname(eachFile);
    const basename = path.basename(eachFile);

    // 查找 index.md 文件
    if (fileInfo.isFile() && basename == 'index.md') {
      let title = `# ${dirname}`;

      console.log('插入标题', title);
    } else if (fileInfo.isDirectory()) {
      // 递归调用
      currtDeep += 1;
      // walk({dirPath:})
    }
  });
}

async function main() {
  const p = path.resolve(target);

  const opts: IOptions = { cwd: p, root: p };

  glob(`/**/*.md`, opts, async (err, files) => {
    if (err) return console.log(err);

    console.log(files.length);

    files.forEach(async (mdFilePath: string) => {
      const res = await fsp.readFile(mdFilePath, {
        encoding: 'utf8',
        flag: 'r',
      });

      const basename = path.basename(mdFilePath, '.md');
      const title = `# ${basename}`;

      if (res.length > 0) {
        let firstLine = res.split('\n')[0].trim();

        if (firstLine.startsWith('# ') && firstLine.includes(`# ${basename}`)) {
          console.log(`【合法】${basename}.md`);
        } else {
          console.log(`【不合法】${basename}.md`);
          console.log(`${firstLine} => ${title}`);
        }
      }
    });
  });
}

const target = 'D:/CPS/MyProject/cps-blog/docs/';

walk({ dirPath: target });
