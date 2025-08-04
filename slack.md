# Slack Conversation Export

**Date Exported:** 2025-07-30
**Messages:** 15
**Type:** Thread

---

## Moses Yu
**Time:** May 6, 2025, 02:32 PM

Is the log for LoadTesting `SeedData` in teamcity available in grafana?

---

## martin.shields
**Time:** May 6, 2025, 02:32 PM

yes

---

## Caleb Heath
**Time:** May 6, 2025, 02:33 PM

Seed data should be under the tasks log group

---

## martin.shields
**Time:** May 6, 2025, 02:34 PM

`@log*group:"global/chaos/service*name/tasks"`

replace `service_name` with the service

---

## Moses Yu
**Time:** May 6, 2025, 02:37 PM

[https://teamcity.sbc.sage.com/buildConfiguration/Deployments*Global_SbcAccountingProjec[…]Data/1476357?buildTab=log&amp;linesState=495&amp;logView=flowAware](https://teamcity.sbc.sage.com/buildConfiguration/Deployments*Global*SbcAccountingProject*2*Chaos*SeedData/1476357?buildTab=log&amp;linesState=495&amp;logView=flowAware)

I can see logs from both `api` and `worker`, but nothing from `tasks`

---

## martin.shields
**Time:** May 6, 2025, 02:38 PM

`@log_group:"global/chaos/project/tasks"`

---

## martin.shields
**Time:** May 6, 2025, 02:38 PM

[https://grafana.logging.sbc-tooling.com/explore?orgId=4&amp;left=%7B%22datasource%22:%2200000000[…]2:%7B%22from%22:%22now-6h%22,%22to%22:%22now%22%7D%7D](https://grafana.logging.sbc-tooling.com/explore?orgId=4&amp;left=%7B%22datasource%22:%22000000006%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22datasource%22:%7B%22type%22:%22elasticsearch%22,%22uid%22:%22000000006%22%7D,%22query%22:%22@log_group:%5C%22global%2Fchaos%2Fproject%2Ftasks%5C%22%22,%22alias%22:%22%22,%22metrics%22:%5B%7B%22id%22:%221%22,%22type%22:%22logs%22,%22settings%22:%7B%22limit%22:%22500%22%7D%7D%5D,%22bucketAggs%22:%5B%5D,%22timeField%22:%22Timestamp%22%7D%5D,%22range%22:%7B%22from%22:%22now-6h%22,%22to%22:%22now%22%7D%7D)

---

## martin.shields
**Time:** May 6, 2025, 02:39 PM

ill have a look

---

## martin.shields
**Time:** May 6, 2025, 02:40 PM

it does look like the one earlier from the day was there but not the 1 from just before, it oculd be the logs have not caught up yet we can check in cloudwatch though

---

## Caleb Heath
**Time:** May 6, 2025, 02:40 PM

I think the logs are delayed

---

## martin.shields
**Time:** May 6, 2025, 02:40 PM

ill take a look

---

## martin.shields
**Time:** May 6, 2025, 02:41 PM

https://grafana.logging.sbc-tooling.com/goto/Cjz1YYxHR?orgId=4

---

## martin.shields
**Time:** May 6, 2025, 02:41 PM

@ yep just delayed streaming to ES, feel free to use that link

---

## Angel Luis Gomez Rodriguez
**Time:** May 6, 2025, 03:02 PM

Is not really delayed, some loggroups are streamed to slowest lambda just to don´t hammer ES

---

## Angel Luis Gomez Rodriguez
**Time:** May 6, 2025, 03:02 PM

tasks is one of them

