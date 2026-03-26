#!/usr/bin/env node
/**
 * decision-helper - 决策助手
 * 帮你做选择，拯救选择困难症！
 */

const fs = require('fs');
const path = require('path');

// 随机选择
function randomChoice(options) {
  if (!options || options.length === 0) {
    return { error: '没有可选择的选项' };
  }
  const choice = options[Math.floor(Math.random() * options.length)];
  return {
    success: true,
    choice,
    message: `🎲 命运选择了... ${choice}！`
  };
}

// 掷骰子
function rollDice(count = 1) {
  const results = [];
  for (let i = 0; i < count; i++) {
    results.push(Math.floor(Math.random() * 6) + 1);
  }
  const total = results.reduce((a, b) => a + b, 0);
  return {
    success: true,
    results,
    total,
    message: count === 1 
      ? `🎲 掷出了 ${results[0]} 点！`
      : `🎲 掷出了 ${results.join(' + ')} = ${total} 点！`
  };
}

// 抛硬币
function flipCoin() {
  const result = Math.random() < 0.5 ? '正面' : '反面';
  const emoji = result === '正面' ? '👑' : '🦅';
  return {
    success: true,
    result,
    message: `${emoji} ${result}！`
  };
}

// 算命/求签
function fortune() {
  const fortunes = [
    { level: '上上签', message: '大吉大利，今晚吃鸡！' },
    { level: '上签', message: '好事将近，保持期待。' },
    { level: '中上签', message: '稳中向好，继续努力。' },
    { level: '中签', message: '平常心，顺其自然。' },
    { level: '中下签', message: '小心谨慎，三思后行。' },
    { level: '下签', message: '多做多错，不如躺平。' },
    { level: '下下签', message: '宜宅家，忌作死。' }
  ];
  
  const fortune = fortunes[Math.floor(Math.random() * fortunes.length)];
  return {
    success: true,
    ...fortune,
    message: `🎋 ${fortune.level}：${fortune.message}`
  };
}

// 利弊分析模板
const analysisTemplates = {
  buy: {
    pros: ['提升效率/体验', '满足感', '可能带来新机会'],
    cons: ['花费金钱', '占用空间', '可能闲置']
  },
  go: {
    pros: ['开阔眼界', '放松身心', '创造回忆'],
    cons: ['花费时间金钱', '可能遇到意外', '旅途劳累']
  },
  eat: {
    pros: ['满足口腹之欲', '补充能量', '社交机会'],
    cons: ['可能不健康', '花费金钱', '可能踩雷']
  },
  default: {
    pros: ['可能带来好处'],
    cons: ['可能带来风险']
  }
};

// 利弊分析
function analyze(topic) {
  const templates = topic.toLowerCase().includes('买') ? analysisTemplates.buy :
                   topic.toLowerCase().includes('去') ? analysisTemplates.go :
                   topic.toLowerCase().includes('吃') ? analysisTemplates.eat :
                   analysisTemplates.default;
  
  return {
    success: true,
    topic,
    pros: templates.pros,
    cons: templates.cons,
    message: `关于「${topic}」的分析：\n\n✅ 好处：\n${templates.pros.map(p => `- ${p}`).join('\n')}\n\n❌ 坏处：\n${templates.cons.map(c => `- ${c}`).join('\n')}\n\n💡 我的建议：跟随你的心！`
  };
}

// CLI 入口
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  let result;
  
  switch (command) {
    case 'choose':
    case '选':
      const options = args.slice(1).join(' ').split(/[,、，或是还有]+/).map(s => s.trim()).filter(Boolean);
      result = randomChoice(options);
      break;
      
    case 'roll':
    case 'dice':
    case '骰子':
      const count = parseInt(args[1]) || 1;
      result = rollDice(Math.min(count, 10));
      break;
      
    case 'coin':
    case 'flip':
    case '硬币':
      result = flipCoin();
      break;
      
    case 'fortune':
    case '算命':
    case '求签':
      result = fortune();
      break;
      
    case 'analyze':
    case '分析':
      const topic = args.slice(1).join(' ');
      result = topic ? analyze(topic) : { error: '请提供要分析的主题' };
      break;
      
    default:
      result = {
        usage: 'decision-helper <command> [options]',
        commands: {
          'choose <options>': '从多个选项中随机选择',
          'roll [count]': '掷骰子（默认1个）',
          'coin': '抛硬币',
          'fortune': '求签',
          'analyze <topic>': '利弊分析'
        }
      };
  }
  
  console.log(JSON.stringify(result, null, 2));
}

main();
