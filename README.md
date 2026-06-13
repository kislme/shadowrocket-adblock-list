# Shadowrocket AdBlock Rule-Set Updater

这个小仓库每天自动把 Johnshall 的 `sr_ad_only.conf` 转成 Shadowrocket `RULE-SET` 可用的 `.list`。

生成两个文件：

- `adblock_shadowrocket_domain_only.list`：推荐，只有域名规则，不含 IP-CIDR，误伤概率更低。
- `adblock_shadowrocket_full.list`：完整规则，包含域名和 IP-CIDR，拦截更强但更容易误伤。

## 用法

1. 在 GitHub 新建一个公开仓库。
2. 把本目录里的所有文件上传到仓库根目录。
3. 进入仓库的 `Actions` 页面，启用 workflow。
4. 手动运行一次 `Update Shadowrocket AdBlock Lists`。
5. 等运行完成后，在 Shadowrocket 配置中添加：

```ini
[Proxy Group]
广告拦截 = select, REJECT, DIRECT

[Rule]
RULE-SET,https://raw.githubusercontent.com/你的用户名/你的仓库名/main/adblock_shadowrocket_domain_only.list,广告拦截
```

把 `你的用户名/你的仓库名` 换成你的 GitHub 用户名和仓库名。

如果要更强的拦截，把 URL 换成：

```ini
https://raw.githubusercontent.com/你的用户名/你的仓库名/main/adblock_shadowrocket_full.list
```

## 建议

优先使用 `domain_only`。如果某个 App 出现空白、登录异常、视频打不开，把小火箭里的 `广告拦截` 组切到 `DIRECT`，即可临时关闭广告拦截。
